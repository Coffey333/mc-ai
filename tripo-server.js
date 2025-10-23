import express from 'express';
import cors from 'cors';
import multer from 'multer';
import FormData from 'form-data';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

const upload = multer({ dest: 'uploads/' });

const API_KEY = process.env.TRIPO_API_KEY;
const TRIPO_API_URL = 'https://api.tripo3d.ai/v2/openapi';

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

app.post('/generate-model', upload.single('image'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No image file provided.' });
  }

  console.log('📸 Received image:', req.file.originalname);
  const imagePath = req.file.path;

  try {
    console.log('📤 Uploading image to Tripo AI...');
    const formData = new FormData();
    formData.append('file', fs.createReadStream(imagePath), {
      filename: req.file.originalname,
      contentType: req.file.mimetype
    });

    const uploadResponse = await fetch(`${TRIPO_API_URL}/upload/sts`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        ...formData.getHeaders()
      },
      body: formData,
      duplex: 'half'
    });

    if (!uploadResponse.ok) {
      throw new Error(`Upload failed: ${await uploadResponse.text()}`);
    }

    const uploadData = await uploadResponse.json();
    const fileToken = uploadData.data.file_token;
    console.log('✅ Got file_token:', fileToken);

    console.log('🎨 Starting 3D generation task...');
    const createTaskResponse = await fetch(`${TRIPO_API_URL}/task`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
      },
      body: JSON.stringify({
        type: 'image_to_model',
        file: { type: 'jpg', file_token: fileToken }
      }),
    });

    if (!createTaskResponse.ok) {
      throw new Error(`Task creation failed: ${await createTaskResponse.text()}`);
    }

    const taskData = await createTaskResponse.json();
    const taskId = taskData.data.task_id;
    console.log('⏳ Task created:', taskId);

    let attempts = 0;
    const maxAttempts = 60;
    let taskStatus = null;

    while (attempts < maxAttempts) {
      attempts++;
      console.log(`🔍 Checking status (attempt ${attempts}/${maxAttempts})...`);

      const statusResponse = await fetch(`${TRIPO_API_URL}/task/${taskId}`, {
        headers: {
          'Authorization': `Bearer ${API_KEY}`,
        },
      });

      if (!statusResponse.ok) {
        throw new Error(`Status check failed: ${await statusResponse.text()}`);
      }

      taskStatus = await statusResponse.json();
      const status = taskStatus.data.status;
      console.log(`📊 Status: ${status}`);

      if (status === 'success') {
        console.log('✅ 3D model generation complete!');
        
        fs.unlinkSync(imagePath);
        
        return res.json({
          success: true,
          taskId: taskId,
          modelUrl: taskStatus.data.output?.model,
          previewUrl: taskStatus.data.output?.rendered_image,
        });
      } else if (status === 'failed') {
        throw new Error('Task failed on Tripo AI side');
      }

      await sleep(5000);
    }

    throw new Error('Task timed out after 5 minutes');

  } catch (error) {
    console.error('❌ Error:', error.message);
    
    if (fs.existsSync(imagePath)) {
      fs.unlinkSync(imagePath);
    }
    
    return res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`🎨 Tripo AI Server listening on port ${port}`);
  if (API_KEY) {
    console.log(`✅ Tripo API Key configured`);
  }
});
