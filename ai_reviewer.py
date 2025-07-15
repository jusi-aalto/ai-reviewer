#!/usr/bin/env python3
"""
AI Reviewer CLI - Command-line interface for generating scholarly peer reviews
"""

import os
import sys
import argparse
import time
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import json

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="AI Reviewer: Generate scholarly peer reviews using specialized agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s manuscript.md                              # Review with default settings
  %(prog)s manuscript.md -m claude -o reviews/        # Use Claude, save to reviews/
  %(prog)s manuscript.md -m all -t 0.5 --max-tokens 8000  # All models, custom settings
  %(prog)s manuscript.md --agents theoretical,empirical   # Only specific agents
  %(prog)s manuscript.md --parallel                       # Parallel agent execution
        """
    )
    
    # Required arguments
    parser.add_argument(
        'manuscript',
        nargs='?',
        help='Path to the manuscript file (.md format)'
    )
    
    # Model selection
    parser.add_argument(
        '-m', '--model',
        choices=['claude', 'chatgpt', 'gemini', 'all'],
        default='claude',
        help='LLM model to use (default: claude)'
    )
    
    # Output settings
    parser.add_argument(
        '-o', '--output-dir',
        default='reviews',
        help='Output directory for review files (default: reviews)'
    )
    
    parser.add_argument(
        '--format',
        choices=['markdown', 'json'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    
    parser.add_argument(
        '--prefix',
        default='',
        help='Prefix for output filenames (default: none)'
    )
    
    # Agent selection
    parser.add_argument(
        '--agents',
        help='Comma-separated list of agents to run (default: all). Options: theoretical,empirical,clarity,significance,structure'
    )
    
    parser.add_argument(
        '--no-editor',
        action='store_true',
        help='Skip Editor\'s Letter generation'
    )
    
    # LLM configuration
    parser.add_argument(
        '--max-tokens',
        type=int,
        help='Maximum tokens for LLM responses (overrides AI_REVIEWER_MAX_TOKENS)'
    )
    
    parser.add_argument(
        '-t', '--temperature',
        type=float,
        help='Temperature for LLM responses (overrides AI_REVIEWER_TEMPERATURE)'
    )
    
    # Execution settings
    parser.add_argument(
        '--parallel',
        action='store_true',
        help='Run agents in parallel (faster but uses more API quota)'
    )
    
    parser.add_argument(
        '--delay',
        type=int,
        default=2,
        help='Delay between agent calls in seconds (default: 2)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=120,
        help='Timeout for each agent in seconds (default: 120)'
    )
    
    # Review settings
    parser.add_argument(
        '--combined',
        action='store_true',
        help='Generate combined review file instead of separate agent files'
    )
    
    parser.add_argument(
        '--journal',
        help='Target journal name (affects review style and standards)'
    )
    
    # Utility options
    parser.add_argument(
        '--list-agents',
        action='store_true',
        help='List available agents and exit'
    )
    
    parser.add_argument(
        '--test-connection',
        action='store_true',
        help='Test API connections and exit'
    )
    
    parser.add_argument(
        '--config',
        help='Path to configuration file (.env format)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Quiet mode (minimal output)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='AI Reviewer 1.0.0'
    )
    
    return parser.parse_args()

def load_configuration(args):
    """Load configuration from environment and command-line arguments."""
    # Load environment variables
    if args.config:
        load_dotenv(args.config)
    else:
        load_dotenv()
    
    # Configuration with command-line overrides
    config = {
        'max_tokens': args.max_tokens or int(os.getenv('AI_REVIEWER_MAX_TOKENS', '6000')),
        'temperature': args.temperature or float(os.getenv('AI_REVIEWER_TEMPERATURE', '0.7')),
        'parallel': args.parallel or os.getenv('AI_REVIEWER_PARALLEL', 'false').lower() == 'true',
        'output_format': args.format or os.getenv('AI_REVIEWER_OUTPUT_FORMAT', 'markdown'),
        'delay': args.delay,
        'timeout': args.timeout,
        'verbose': args.verbose,
        'quiet': args.quiet
    }
    
    return config

def list_available_agents():
    """List all available agents."""
    agents = {
        'theoretical': 'Theoretical Framework & Hypothesis Development Specialist',
        'empirical': 'Empirical Identification & Methods Specialist',
        'clarity': 'Conceptual Clarity & Presentation Specialist',
        'significance': 'Economic Significance & External Validity Specialist',
        'structure': 'Paper Structure & Presentation Specialist'
    }
    
    print("Available Agents:")
    for agent_id, description in agents.items():
        print(f"  {agent_id:<12} - {description}")
    
    return agents

def test_api_connections(models):
    """Test API connections for specified models."""
    print("Testing API connections...")
    
    results = {}
    for model in models:
        try:
            # Import and test each model
            if model == 'claude':
                import anthropic
                api_key = os.getenv('ANTHROPIC_API_KEY')
                if api_key and 'placeholder' not in api_key:
                    client = anthropic.Anthropic(api_key=api_key)
                    response = client.messages.create(
                        model="claude-sonnet-4-0",
                        max_tokens=100,
                        temperature=0.7,
                        messages=[{"role": "user", "content": "Test"}]
                    )
                    results[model] = "✓ Connected"
                else:
                    results[model] = "✗ API key not configured"
            
            elif model == 'chatgpt':
                import openai
                api_key = os.getenv('OPENAI_API_KEY')
                if api_key and 'placeholder' not in api_key:
                    client = openai.OpenAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        max_tokens=100,
                        temperature=0.7,
                        messages=[{"role": "user", "content": "Test"}]
                    )
                    results[model] = "✓ Connected"
                else:
                    results[model] = "✗ API key not configured"
            
            elif model == 'gemini':
                import google.generativeai as genai
                api_key = os.getenv('GOOGLE_API_KEY')
                if api_key and 'placeholder' not in api_key:
                    genai.configure(api_key=api_key)
                    model_obj = genai.GenerativeModel('gemini-2.5-pro')
                    response = model_obj.generate_content("Test")
                    results[model] = "✓ Connected"
                else:
                    results[model] = "✗ API key not configured"
                    
        except Exception as e:
            results[model] = f"✗ Error: {str(e)[:50]}..."
    
    for model, status in results.items():
        print(f"  {model.upper():<8} - {status}")
    
    return results

def get_agent_prompts():
    """Get specialized prompts for each of the 5 reviewer agents."""
    return {
        "theoretical": {
            "title": "Theoretical Framework & Hypothesis Development Specialist",
            "prompt": """You are Reviewer #1 - Theoretical Framework & Hypothesis Development Specialist.

Provide a comprehensive review focusing on:
- Theoretical grounding and framework development
- Hypothesis development and justification
- Literature integration and positioning
- Conceptual clarity and logical flow

Structure your review as a formal reviewer report with:
- Brief summary of the theoretical approach
- Major strengths and weaknesses
- Specific detailed comments with section references
- Recommendations for improvement
- Overall assessment and recommendation (Accept/Minor Revision/Major Revision/Reject)

Be constructive, specific, and thorough in your feedback."""
        },
        
        "empirical": {
            "title": "Empirical Identification & Methods Specialist",
            "prompt": """You are Reviewer #2 - Empirical Identification & Methods Specialist.

Provide a comprehensive review focusing on:
- Identification strategy and causal inference
- Data quality and sample construction
- Econometric specifications and robustness
- Measurement validity and reliability

Structure your review as a formal reviewer report with:
- Brief summary of the empirical approach
- Major strengths and weaknesses
- Specific detailed comments with section references
- Recommendations for improvement
- Overall assessment and recommendation (Accept/Minor Revision/Major Revision/Reject)

Be rigorous, technical, and constructive in your feedback."""
        },
        
        "clarity": {
            "title": "Conceptual Clarity & Presentation Specialist",
            "prompt": """You are Reviewer #3 - Conceptual Clarity & Presentation Specialist.

Provide a comprehensive review focusing on:
- Writing quality and clarity
- Presentation and organization
- Figures, tables, and visual aids
- Overall manuscript structure and flow

Structure your review as a formal reviewer report with:
- Brief summary of presentation quality
- Major strengths and weaknesses
- Specific detailed comments with section references
- Recommendations for improvement
- Overall assessment and recommendation (Accept/Minor Revision/Major Revision/Reject)

Be detailed, constructive, and focused on enhancing communication."""
        },
        
        "significance": {
            "title": "Economic Significance & External Validity Specialist",
            "prompt": """You are Reviewer #4 - Economic Significance & External Validity Specialist.

Provide a comprehensive review focusing on:
- Economic significance and practical importance
- External validity and generalizability
- Policy and practical implications
- Overall contribution to the field

Structure your review as a formal reviewer report with:
- Brief summary of the contribution and significance
- Major strengths and weaknesses
- Specific detailed comments with section references
- Recommendations for improvement
- Overall assessment and recommendation (Accept/Minor Revision/Major Revision/Reject)

Be pragmatic, insightful, and focused on real-world impact."""
        },
        
        "structure": {
            "title": "Paper Structure & Presentation Specialist",
            "prompt": """You are Reviewer #5 - Paper Structure & Presentation Specialist.

Provide a comprehensive review focusing on:
- Adherence to empirical paper conventions
- Table and figure presentation
- Organization and logical flow
- Professional presentation standards

Structure your review as a formal reviewer report with:
- Brief summary of structural and presentation quality
- Major strengths and weaknesses
- Specific detailed comments with section references
- Recommendations for improvement
- Overall assessment and recommendation (Accept/Minor Revision/Major Revision/Reject)

Be focused on structural conventions and professional presentation."""
        }
    }

def call_llm_api(model, prompt, manuscript, config):
    """Call the appropriate LLM API."""
    max_tokens = config['max_tokens']
    temperature = config['temperature']
    
    if model == 'claude':
        import anthropic
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key or 'placeholder' in api_key:
            return None
        
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-0",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": f"{prompt}\n\nMANUSCRIPT:\n{manuscript}"}]
        )
        return response.content[0].text
    
    elif model == 'chatgpt':
        import openai
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or 'placeholder' in api_key:
            return None
        
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"MANUSCRIPT:\n{manuscript}"}
            ]
        )
        return response.choices[0].message.content
    
    elif model == 'gemini':
        import google.generativeai as genai
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key or 'placeholder' in api_key:
            return None
        
        genai.configure(api_key=api_key)
        model_obj = genai.GenerativeModel('gemini-2.5-pro')
        response = model_obj.generate_content(
            f"{prompt}\n\nMANUSCRIPT:\n{manuscript}",
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
        )
        return response.text
    
    return None

def generate_review(manuscript_path, model, selected_agents, config, args):
    """Generate review with specified model and agents."""
    # Load manuscript
    try:
        with open(manuscript_path, 'r', encoding='utf-8') as f:
            manuscript = f.read()
    except FileNotFoundError:
        print(f"Error: Manuscript file '{manuscript_path}' not found.")
        return False
    
    # Extract title
    import re
    title_match = re.search(r'^#\s+(.+)$', manuscript, re.MULTILINE)
    title = title_match.group(1) if title_match else "Untitled"
    
    if not config['quiet']:
        print(f"Generating review for: {title}")
        print(f"Model: {model.upper()}")
        print(f"Agents: {', '.join(selected_agents)}")
    
    # Get agent prompts
    agent_prompts = get_agent_prompts()
    
    # Generate individual agent reports
    if config['verbose']:
        print("Generating individual agent reports...")
    
    agent_files = {}
    agent_decisions = {}
    
    for agent_name in selected_agents:
        if agent_name not in agent_prompts:
            print(f"Warning: Unknown agent '{agent_name}', skipping...")
            continue
        
        if config['verbose']:
            print(f"  Running {agent_name} agent...")
        
        try:
            agent_config = agent_prompts[agent_name]
            response = call_llm_api(model, agent_config["prompt"], manuscript, config)
            
            if response:
                # Create filename
                prefix = f"{args.prefix}_" if args.prefix else ""
                filename = f"{prefix}reviewer_{agent_name}_{model}.md"
                filepath = os.path.join(args.output_dir, filename)
                
                # Create agent report document
                agent_content = f"""# Reviewer Report - {agent_config["title"]}

## Model: {model.upper()}
## Manuscript: {title}
## Agent: {agent_config["title"]}
## Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

{response}

---

*Generated by AI Reviewer System ({model.upper()} Model)*  
*Agent: {agent_config["title"]}*
*Configuration: MAX_TOKENS={config['max_tokens']}, TEMPERATURE={config['temperature']}*
"""
                
                # Save agent report
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(agent_content)
                
                agent_files[agent_name] = filename
                
                # Extract decision (simple heuristic)
                response_lower = response.lower()
                if "reject" in response_lower:
                    agent_decisions[agent_name] = "Reject"
                elif "major revision" in response_lower:
                    agent_decisions[agent_name] = "Major Revision"
                elif "minor revision" in response_lower:
                    agent_decisions[agent_name] = "Minor Revision"
                else:
                    agent_decisions[agent_name] = "Accept"
                
                if config['verbose']:
                    print(f"    ✓ {agent_name} report saved to {filename} ({len(response)} chars)")
            else:
                if config['verbose']:
                    print(f"    ✗ {agent_name} report failed")
                
        except Exception as e:
            if config['verbose']:
                print(f"    ✗ {agent_name} error: {e}")
        
        # Delay between agents if not parallel
        if not config['parallel'] and agent_name != selected_agents[-1]:
            time.sleep(config['delay'])
    
    # Generate editor's letter if requested
    if not args.no_editor and agent_files:
        if config['verbose']:
            print("Generating editor's letter...")
        
        # Determine overall editorial decision
        decisions = list(agent_decisions.values())
        reject_count = decisions.count("Reject")
        major_count = decisions.count("Major Revision")
        minor_count = decisions.count("Minor Revision")
        accept_count = decisions.count("Accept")
        
        if reject_count >= 2:
            editorial_decision = "Reject"
        elif major_count >= 2:
            editorial_decision = "Major Revision"
        elif minor_count >= 2:
            editorial_decision = "Minor Revision"
        else:
            editorial_decision = "Accept"
        
        # Create editor prompt
        reviewer_files_list = "\n".join([f"- {filename}" for filename in agent_files.values()])
        
        editor_prompt = f"""You are the Editor-in-Chief of a top-tier academic journal. You have received a manuscript titled "{title}" and have received detailed reviews from {len(agent_files)} specialized reviewers.

The reviewers have provided their individual reports in separate files:
{reviewer_files_list}

Their individual recommendations are:
{chr(10).join([f"- {agent_prompts[agent_name]['title']}: {decision}" for agent_name, decision in agent_decisions.items()])}

Based on this collective feedback, your editorial decision should be: {editorial_decision}

Please write a professional Editorial Decision Letter that:
1. Thanks the authors for their submission
2. Announces the editorial decision clearly
3. Provides a synthesis of the key themes from the reviewers
4. References the individual reviewer reports by filename
5. Gives strategic guidance for revision (if applicable)
6. Sets clear expectations for next steps

The letter should be 1000-1200 words and maintain a professional academic tone. 

IMPORTANT: Do NOT reproduce the full content of the individual reviewer reports. Instead, reference them by filename and provide a synthesized overview of the main themes and concerns.

Please provide a comprehensive editorial letter that appropriately references the individual reviewer reports by filename."""
        
        if args.journal:
            editor_prompt += f"\n\nThis review is for {args.journal}. Please adjust the tone and standards accordingly."
        
        editor_response = call_llm_api(model, editor_prompt, "", config)
        
        if editor_response:
            # Create editorial letter file
            prefix = f"{args.prefix}_" if args.prefix else ""
            editor_filename = f"{prefix}editorial_letter_{model}.md"
            editor_filepath = os.path.join(args.output_dir, editor_filename)
            
            editor_content = f"""# AI Reviewer - Editorial Decision Letter

## Model: {model.upper()}
## Manuscript: {title}
## Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
## Configuration: MAX_TOKENS={config['max_tokens']}, TEMPERATURE={config['temperature']}

---

{editor_response}

---

## Individual Reviewer Reports

The following individual reviewer reports were considered in this editorial decision:

{chr(10).join([f"- **{agent_prompts[agent_name]['title']}**: `{filename}`" for agent_name, filename in agent_files.items()])}

Please refer to the individual reviewer reports for detailed feedback and recommendations.

---

*Generated by AI Reviewer System ({model.upper()} Model)*  
*Editorial Decision Letter with {len(agent_files)} Individual Reviewer Reports*
*Configuration: MAX_TOKENS={config['max_tokens']}, TEMPERATURE={config['temperature']}*
"""
            
            with open(editor_filepath, 'w', encoding='utf-8') as f:
                f.write(editor_content)
            
            if config['verbose']:
                print(f"  ✓ Editor's letter saved to {editor_filename}")
    
    # Summary
    if not config['quiet']:
        print(f"\n✓ Review generation completed for {model.upper()}")
        print(f"  Output directory: {args.output_dir}")
        print(f"  Agent reports: {len(agent_files)} files")
        if not args.no_editor:
            print(f"  Editorial decision: {editorial_decision}")
    
    return True

def main():
    """Main CLI entry point."""
    args = parse_arguments()
    
    # Handle utility options
    if args.list_agents:
        list_available_agents()
        return
    
    if args.test_connection:
        models = ['claude', 'chatgpt', 'gemini'] if args.model == 'all' else [args.model]
        test_api_connections(models)
        return
    
    # Validate manuscript file
    if not args.manuscript:
        print("Error: Manuscript file is required.")
        print("Use --help for usage information.")
        sys.exit(1)
    
    if not os.path.exists(args.manuscript):
        print(f"Error: Manuscript file '{args.manuscript}' not found.")
        sys.exit(1)
    
    # Load configuration
    config = load_configuration(args)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Determine agents to run
    if args.agents:
        selected_agents = [agent.strip() for agent in args.agents.split(',')]
    else:
        selected_agents = ['theoretical', 'empirical', 'clarity', 'significance', 'structure']
    
    # Determine models to use
    if args.model == 'all':
        models = ['claude', 'chatgpt', 'gemini']
    else:
        models = [args.model]
    
    # Print configuration if verbose
    if config['verbose']:
        print(f"AI Reviewer Configuration:")
        print(f"  Manuscript: {args.manuscript}")
        print(f"  Models: {', '.join(models)}")
        print(f"  Agents: {', '.join(selected_agents)}")
        print(f"  Output: {args.output_dir}")
        print(f"  Format: {args.format}")
        print(f"  Max Tokens: {config['max_tokens']}")
        print(f"  Temperature: {config['temperature']}")
        print(f"  Parallel: {config['parallel']}")
        print()
    
    # Run review for each model
    all_success = True
    for model in models:
        if not config['quiet']:
            print(f"{'='*50}")
            print(f"Generating review with {model.upper()}")
            print(f"{'='*50}")
        
        success = generate_review(args.manuscript, model, selected_agents, config, args)
        
        if not success:
            all_success = False
            if not config['quiet']:
                print(f"✗ {model.upper()} review failed")
        
        # Pause between models
        if model != models[-1]:
            time.sleep(config['delay'])
    
    if not config['quiet']:
        if all_success:
            print(f"\n✅ All reviews completed successfully!")
        else:
            print(f"\n⚠️  Some reviews failed")
        print(f"📁 Output directory: {args.output_dir}")

if __name__ == '__main__':
    main()