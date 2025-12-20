#!/bin/bash
# Run Rfam test suite with various options

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Rfam Website Test Suite           ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo ""

# Check if virtual environment should be created
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo -e "${GREEN}Virtual environment created and dependencies installed.${NC}"
    echo ""
else
    source venv/bin/activate
    echo -e "${GREEN}Using existing virtual environment.${NC}"
    echo ""
fi

# Default options
RUN_MODE="all"
PARALLEL=""
REPORT=""
MARKERS=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --fast)
            RUN_MODE="fast"
            shift
            ;;
        --ui)
            MARKERS="-m ui"
            shift
            ;;
        --api)
            MARKERS="-m api"
            shift
            ;;
        --search)
            MARKERS="-m search"
            shift
            ;;
        --integration)
            MARKERS="-m integration"
            shift
            ;;
        --parallel)
            PARALLEL="-n auto"
            shift
            ;;
        --report)
            REPORT="--html=report.html --self-contained-html"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --fast          Run only fast tests (exclude slow tests)"
            echo "  --ui            Run only UI tests"
            echo "  --api           Run only API tests"
            echo "  --search        Run only search tests"
            echo "  --integration   Run only integration tests"
            echo "  --parallel      Run tests in parallel"
            echo "  --report        Generate HTML report"
            echo "  --help, -h      Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                          # Run all tests"
            echo "  $0 --fast --parallel        # Run fast tests in parallel"
            echo "  $0 --api --report           # Run API tests and generate report"
            echo "  $0 --ui --parallel          # Run UI tests in parallel"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Set markers based on run mode
if [ "$RUN_MODE" = "fast" ]; then
    MARKERS="-m 'not slow'"
fi

# Build pytest command
PYTEST_CMD="pytest $MARKERS $PARALLEL $REPORT"

echo -e "${BLUE}Running tests with command:${NC}"
echo -e "${GREEN}$PYTEST_CMD${NC}"
echo ""

# Run tests
if eval $PYTEST_CMD; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     All tests passed! ✓                ║${NC}"
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"

    if [ -n "$REPORT" ]; then
        echo ""
        echo -e "${BLUE}HTML report generated: report.html${NC}"
        echo -e "${BLUE}Open with: open report.html (macOS) or xdg-open report.html (Linux)${NC}"
    fi

    exit 0
else
    echo ""
    echo -e "${RED}╔════════════════════════════════════════╗${NC}"
    echo -e "${RED}║     Some tests failed ✗                ║${NC}"
    echo -e "${RED}╔════════════════════════════════════════╗${NC}"

    if [ -n "$REPORT" ]; then
        echo ""
        echo -e "${YELLOW}HTML report generated: report.html${NC}"
        echo -e "${YELLOW}Open with: open report.html (macOS) or xdg-open report.html (Linux)${NC}"
    fi

    exit 1
fi
