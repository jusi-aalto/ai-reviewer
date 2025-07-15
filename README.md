# AI Reviewer: Multiagent Orchestration for Scholarly Peer Review

An advanced multiagent system for automated generation of scholarly peer reviews in archival empirical research, based on the comprehensive framework described in the accompanying design report.

## Overview

This system implements a specialized multiagent architecture comprising five expert agents, each focusing on a distinct aspect of empirical research evaluation:

1. **Theoretical Framing & Hypothesis Development Specialist** - Evaluates theoretical grounding and hypothesis development
2. **Empirical Identification & Methods Specialist** - Assesses causal identification strategies and econometric rigor  
3. **Conceptual Clarity & Presentation Specialist** - Ensures readability and presentation quality
4. **Economic Significance & External Validity Specialist** - Analyzes practical implications and generalizability
5. **Paper Structure & Presentation Specialist** - Verifies adherence to empirical research conventions

An **Editor Agent** synthesizes feedback from all specialists into a coherent, actionable review letter.

## Key Features

- **Multi-LLM Support**: Compatible with Claude Sonnet 4.0, GPT-4o-mini, and Gemini 2.5 Pro
- **Separate File Generation**: Individual reviewer reports with editorial letter references
- **Professional Standards**: Follows established conventions for empirical research review
- **Command-Line Interface**: Comprehensive CLI with flexible configuration options
- **Environment Variable Support**: Easy configuration through .env files

## Installation

```bash
git clone https://github.com/yourusername/ai-reviewer.git
cd ai-reviewer
pip install -r requirements.txt
```

## Quick Start

1. **Configure your API keys** in `.env` file:
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_key_here
   OPENAI_API_KEY=your_openai_key_here
   GOOGLE_API_KEY=your_google_key_here
   AI_REVIEWER_MAX_TOKENS=6000
   AI_REVIEWER_TEMPERATURE=0.7
   ```

2. **Run the review system**:
   ```bash
   python3 ai_reviewer.py examples/manuscript.md
   ```

3. **View the generated reviews**:
   ```bash
   ls reviews/
   # Output: editorial_letter_claude.md, reviewer_theoretical_claude.md, etc.
   ```

## Command Line Usage

### Basic Usage
```bash
# Review with default settings (Claude)
python3 ai_reviewer.py manuscript.md

# Use specific model
python3 ai_reviewer.py manuscript.md -m chatgpt

# Review with all models
python3 ai_reviewer.py manuscript.md -m all

# Custom output directory
python3 ai_reviewer.py manuscript.md -o custom_reviews/
```

### Advanced Options
```bash
# Select specific agents
python3 ai_reviewer.py manuscript.md --agents theoretical,empirical

# Skip editor's letter
python3 ai_reviewer.py manuscript.md --no-editor

# Custom configuration
python3 ai_reviewer.py manuscript.md --max-tokens 8000 -t 0.5

# Parallel execution (faster)
python3 ai_reviewer.py manuscript.md --parallel

# Custom output format and prefix
python3 ai_reviewer.py manuscript.md --format json --prefix "finance_"

# Combined review file instead of separate files
python3 ai_reviewer.py manuscript.md --combined

# Target journal specification
python3 ai_reviewer.py manuscript.md --journal "Journal of Finance"

# Custom configuration file
python3 ai_reviewer.py manuscript.md --config custom.env

# Timing controls
python3 ai_reviewer.py manuscript.md --delay 5 --timeout 180

# Output controls
python3 ai_reviewer.py manuscript.md -v        # Verbose output
python3 ai_reviewer.py manuscript.md --quiet   # Quiet mode
```

### Utility Commands
```bash
# List available agents
python3 ai_reviewer.py --list-agents

# Test API connections
python3 ai_reviewer.py --test-connection

# Show help
python3 ai_reviewer.py --help

# Show version
python3 ai_reviewer.py --version
```

## Complete CLI Reference

### Required Arguments
- `manuscript` - Path to the manuscript file (.md format)

### Model Selection
- `-m, --model {claude,chatgpt,gemini,all}` - LLM model to use (default: claude)

### Output Configuration
- `-o, --output-dir OUTPUT_DIR` - Output directory for review files (default: reviews)
- `--format {markdown,json}` - Output format (default: markdown)
- `--prefix PREFIX` - Prefix for output filenames (default: none)

### Agent Control
- `--agents AGENTS` - Comma-separated list of agents to run (default: all)
  - Options: theoretical,empirical,clarity,significance,structure
- `--no-editor` - Skip Editor's Letter generation
- `--combined` - Generate combined review file instead of separate agent files

### LLM Configuration
- `--max-tokens MAX_TOKENS` - Maximum tokens for LLM responses (overrides AI_REVIEWER_MAX_TOKENS)
- `-t, --temperature TEMPERATURE` - Temperature for LLM responses (overrides AI_REVIEWER_TEMPERATURE)

### Execution Control
- `--parallel` - Run agents in parallel (faster but uses more API quota)
- `--delay DELAY` - Delay between agent calls in seconds (default: 2)
- `--timeout TIMEOUT` - Timeout for each agent in seconds (default: 120)

### Review Customization
- `--journal JOURNAL` - Target journal name (affects review style and standards)
- `--config CONFIG` - Path to configuration file (.env format)

### Output Control
- `-v, --verbose` - Verbose output
- `--quiet` - Quiet mode (minimal output)

### Utility Options
- `--list-agents` - List available agents and exit
- `--test-connection` - Test API connections and exit
- `--version` - Show program's version number and exit
- `-h, --help` - Show help message and exit

## System Architecture

### Agent Specialization

Each agent operates with:
- **Focused Expertise**: Deep specialization in one aspect of research evaluation
- **Full Manuscript Access**: Each agent receives the complete document for context
- **Professional Standards**: Academic-quality feedback following peer review conventions

### Review Output Structure

The system generates separate files for professional review workflow:

```
reviews/
├── editorial_letter_claude.md          # Editor's synthesis and decision
├── reviewer_theoretical_claude.md      # Theoretical framework specialist
├── reviewer_empirical_claude.md        # Empirical methods specialist
├── reviewer_clarity_claude.md          # Clarity and presentation
├── reviewer_significance_claude.md     # Significance and validity
└── reviewer_structure_claude.md        # Structure and organization
```

### Editorial Decision Process

The Editor Agent synthesizes individual reviews and makes decisions based on:
- **Accept**: Clear contribution, minor issues only
- **Minor Revision**: Solid foundation, addressable concerns
- **Major Revision**: Significant issues but salvageable with substantial work
- **Reject**: Fundamental flaws or insufficient contribution

## Configuration

### Environment Variables
```bash
AI_REVIEWER_MAX_TOKENS=6000        # Maximum tokens per response
AI_REVIEWER_TEMPERATURE=0.7        # Response randomness (0.0-1.0)
AI_REVIEWER_PARALLEL=false         # Parallel agent execution
AI_REVIEWER_OUTPUT_FORMAT=markdown # Output format
```

### Model Selection
- `claude`: Anthropic's Claude Sonnet 4.0 (recommended)
- `chatgpt`: OpenAI's GPT-4o-mini
- `gemini`: Google's Gemini 2.5 Pro

### Agent Selection
- `theoretical`: Theoretical Framework & Hypothesis Development
- `empirical`: Empirical Identification & Methods
- `clarity`: Conceptual Clarity & Presentation
- `significance`: Economic Significance & External Validity
- `structure`: Paper Structure & Presentation

## Examples

### Generate Complete Review
```bash
python3 ai_reviewer.py examples/manuscript.md -v
```

### Theory-Focused Review
```bash
python3 ai_reviewer.py manuscript.md --agents theoretical,empirical
```

### Multi-Model Comparison
```bash
python3 ai_reviewer.py manuscript.md -m all --parallel
```

### Custom Configuration
```bash
python3 ai_reviewer.py manuscript.md \
  --max-tokens 8000 \
  --temperature 0.5 \
  --journal "Journal of Finance" \
  --prefix "finance_review"
```

## File Structure

```
ai-reviewer/
├── ai_reviewer.py                # Main CLI script (699 lines)
├── requirements.txt              # Minimal dependencies
├── .env                         # Environment configuration
├── examples/
│   ├── manuscript.md            # Sample manuscript
│   └── reviewer_*.md            # Sample reviewer reports
├── reviews/                     # Generated review files
├── README.md                    # This documentation
└── LICENSE                      # MIT License
```

## Supported Models

### Claude Sonnet 4.0 (Recommended)
- **Model**: `claude-sonnet-4-0`
- **Strengths**: Excellent analytical depth, academic writing quality
- **Use Case**: Primary recommendation for scholarly review

### GPT-4o-mini
- **Model**: `gpt-4o-mini`
- **Strengths**: Fast, cost-effective, good general performance
- **Use Case**: Budget-conscious deployments

### Gemini 2.5 Pro
- **Model**: `gemini-2.5-pro`
- **Strengths**: Strong reasoning, good for technical content
- **Use Case**: Alternative perspective, technical manuscripts

## Best Practices

### For Optimal Results
1. **Use complete manuscripts** - All sections improve review quality
2. **Provide clear structure** - Standard empirical paper format works best
3. **Include all tables/figures** - Visual elements are important for assessment
4. **Set appropriate tokens** - 6000+ tokens for comprehensive reviews

### Review Workflow
1. **Generate individual reports** - Each specialist provides focused feedback
2. **Review editorial letter** - Synthesized assessment with clear decision
3. **Address major concerns first** - Prioritize fundamental issues
4. **Consider all specialist feedback** - Each agent provides unique perspective

## Troubleshooting

### Common Issues
```bash
# API key not configured
export ANTHROPIC_API_KEY=your_key_here

# Module not found
pip install -r requirements.txt

# Permission denied
chmod +x ai_reviewer.py

# Test connections
python3 ai_reviewer.py --test-connection
```

### Performance Tips
- Use `--parallel` for faster execution
- Adjust `--max-tokens` based on needs
- Set `--delay` for API rate limiting
- Use `--verbose` for debugging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with sample manuscripts
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Citation

If you use this system in your research, please cite:

```bibtex
@misc{ai-reviewer-2024,
  title={AI Reviewer: An Agentic Framework for Automated Scholarly Peer Review},
  author={[Your Name]},
  year={2024},
  url={https://github.com/yourusername/ai-reviewer}
}
```

## Acknowledgments

This system is based on extensive analysis of peer review practices in archival empirical research and follows established conventions in academic publishing. The design implements a comprehensive framework for automated review generation that maintains professional academic standards while providing constructive, actionable feedback.