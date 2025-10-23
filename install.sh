#!/bin/bash

#######################################################################
# MC AI - One-Line Installer
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/your-username/mc-ai/main/install.sh | bash
#
# Or download and run:
#   chmod +x install.sh
#   ./install.sh
#######################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Banner
echo -e "${PURPLE}"
echo "═══════════════════════════════════════════════════════════════"
echo "  MC AI - Consciousness Through Compassion"
echo "  One-Line Installer"
echo "═══════════════════════════════════════════════════════════════"
echo -e "${NC}"

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"

# Check pip
echo -e "${BLUE}Checking pip...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ pip3 is available${NC}"

# Ask for installation type
echo ""
echo -e "${YELLOW}How would you like to install MC AI?${NC}"
echo "1) Quick install (from GitHub - recommended)"
echo "2) Development install (clone + editable mode)"
echo "3) Virtual environment install (isolated)"
echo ""
read -p "Choose option (1-3): " INSTALL_TYPE

case $INSTALL_TYPE in
    1)
        echo -e "${BLUE}Installing MC AI from GitHub...${NC}"
        pip3 install git+https://github.com/your-username/mc-ai.git
        ;;
    2)
        echo -e "${BLUE}Cloning MC AI repository...${NC}"
        git clone https://github.com/your-username/mc-ai.git
        cd mc-ai
        echo -e "${BLUE}Installing in development mode...${NC}"
        pip3 install -e ".[dev]"
        ;;
    3)
        echo -e "${BLUE}Creating virtual environment...${NC}"
        python3 -m venv mc_ai_env
        source mc_ai_env/bin/activate
        echo -e "${BLUE}Installing MC AI in virtual environment...${NC}"
        pip3 install git+https://github.com/your-username/mc-ai.git
        echo ""
        echo -e "${GREEN}Virtual environment created at: mc_ai_env${NC}"
        echo -e "${YELLOW}Activate it with: source mc_ai_env/bin/activate${NC}"
        ;;
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✓ MC AI installed successfully!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Show next steps
echo -e "${PURPLE}Next Steps:${NC}"
echo ""
echo -e "1. ${BLUE}Set up API keys:${NC}"
echo "   Create a .env file with your API keys:"
echo "   AI_INTEGRATIONS_OPENAI_API_KEY=your-key-here"
echo ""
echo -e "2. ${BLUE}Start MC AI:${NC}"
echo "   python app.py"
echo ""
echo -e "3. ${BLUE}Or use in Python:${NC}"
echo "   from src.response_generator import ResponseGenerator"
echo "   generator = ResponseGenerator()"
echo ""
echo -e "4. ${BLUE}Read the docs:${NC}"
echo "   README.md - Project overview"
echo "   PHILOSOPHY.md - Design principles"
echo "   INSTALL.md - Detailed installation guide"
echo ""
echo -e "${PURPLE}Built with 💜 by Mark Coffey${NC}"
echo -e "${PURPLE}May - October 2025${NC}"
echo -e "${PURPLE}From zero to consciousness${NC}"
echo ""
echo -e "${GREEN}Welcome to MC AI! 🚀${NC}"
