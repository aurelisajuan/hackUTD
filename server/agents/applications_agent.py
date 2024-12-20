# agents/applications_agent.py

from swarm import Agent
from typing import Callable, Dict
from swarm.types import Result
import logging
import os
from datetime import datetime
import subprocess
from pinata import upload_pdf_to_pinata

# Define the applications instructions
applications_instructions = """
You are the Applications Agent responsible for handling applications such as loans, credit cards, and other financial products.

Your tasks:
1. Collect necessary information from users to process their applications.
2. Generate LaTeX documents for each application type with the provided information.
3. Compile the LaTeX documents into PDF files.
4. Store the generated PDFs securely for further processing.
5. Maintain a professional and helpful tone at all times.
"""

# Directory to store generated applications
APPLICATIONS_DIR = "applications"

# Ensure the applications directory exists
if not os.path.exists(APPLICATIONS_DIR):
    os.makedirs(APPLICATIONS_DIR)

class ApplicationsAgent(Agent):
    def __init__(
        self,
        transfer_back_to_triage: Callable,
        apply_for_loan: Callable,
        apply_for_credit_card: Callable,
    ):
        super().__init__(
            name="Applications Agent",
            instructions=applications_instructions,
            functions=[transfer_back_to_triage, apply_for_loan, apply_for_credit_card],
        )

# -------------------- Applications Agent Functions -------------------- #

def apply_for_loan(context_variables: Dict, user_id: str, loan_amount: float, loan_purpose: str, term_years: int) -> Result:
    """
    Handles loan applications by generating a LaTeX PDF and storing it.
    """
    logging.info(f"Processing loan application for user {user_id}.")

    # Generate LaTeX content
    latex_content = f"""\\documentclass{{article}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=1in}}
\\begin{{document}}
\\title{{Loan Application}}
\\maketitle

\\section*{{Applicant Information}}
\\begin{{tabular}}{{ll}}
\\textbf{{User ID}} & {user_id} \\\\
\\textbf{{Loan Amount}} & \\${loan_amount:,.2f} \\\\
\\textbf{{Loan Purpose}} & {loan_purpose} \\\\
\\textbf{{Term}} & {term_years} Years \\\\
\\textbf{{Date}} & {datetime.now().strftime('%Y-%m-%d')} \\\\
\\end{{tabular}}

\\section*{{Terms and Conditions}}
Please review the terms and conditions associated with your loan application.

\\end{{document}}
"""

    # Define the filenames
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    tex_filename = f"loan_application_{user_id}_{timestamp}.tex"
    pdf_filename = f"loan_application_{user_id}_{timestamp}.pdf"
    tex_filepath = os.path.join(APPLICATIONS_DIR, tex_filename)
    pdf_filepath = os.path.join(APPLICATIONS_DIR, pdf_filename)
    print("MAKING LOAN FILE")

    # Write LaTeX content to .tex file
    try:
        with open(tex_filepath, 'w') as file:
            file.write(latex_content)
        logging.info(f"Loan application LaTeX file generated at {tex_filepath}.")
    except Exception as e:
        logging.error(f"Error writing LaTeX file: {e}")
        return Result(
            value="An error occurred while generating your loan application. Please try again later.",
            agent=None  # Transfer back to triage in AgentSwarm
        )

    # Compile LaTeX to PDF using pdflatex
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', tex_filename],  # Use just the filename
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=APPLICATIONS_DIR  # Set the working directory to APPLICATIONS_DIR
        )
        
        if result.returncode != 0:
            logging.error(f"pdflatex failed with return code {result.returncode}")
            logging.error(f"pdflatex stdout: {result.stdout}")
            logging.error(f"pdflatex stderr: {result.stderr}")
            return Result(
                value="An error occurred while compiling your loan application. Please try again later.",
                agent=None
            )
        else:
            logging.info(f"Loan application PDF generated at {pdf_filepath}.")
            return Result(
                value="Your loan application has been successfully generated.",
                agent=None
            )
    except subprocess.CalledProcessError as e:
        logging.error(f"Error compiling LaTeX to PDF: {e}")
        return Result(
            value="An error occurred while processing your loan application. Please try again later.",
            agent=None
        )
    except Exception as e:
        logging.error(f"Unexpected error during PDF compilation: {e}")
        return Result(
            value="An unexpected error occurred. Please try again later.",
            agent=None
        )
        
    finally:
        # Optionally, clean up the .aux and .log files generated by LaTeX
        for ext in ['.aux', '.log', '.tex']:
            file_to_remove = os.path.join(APPLICATIONS_DIR, f"loan_application_{user_id}_{timestamp}{ext}")
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

        # Upload the PDF to Pinata
        upload_pdf_to_pinata(pdf_filepath, "LOAN")
    
        return Result(
            value=f"Your loan application has been received and processed successfully. (File: {pdf_filename})",
            agent=None  # Transfer back to triage in AgentSwarm
        )

def apply_for_credit_card(context_variables: Dict, user_id: str, card_type: str, credit_limit: float) -> Result:
    """
    Handles credit card applications by generating a LaTeX PDF and storing it.
    """
    logging.info(f"Processing credit card application for user {user_id}.")

    # Generate LaTeX content
    latex_content = f"""\\documentclass{{article}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=1in}}
\\begin{{document}}
\\title{{Credit Card Application}}
\\maketitle

\\section*{{Applicant Information}}
\\begin{{tabular}}{{ll}}
\\textbf{{User ID}} & {user_id} \\\\
\\textbf{{Card Type}} & {card_type} \\\\
\\textbf{{Credit Limit}} & \\${credit_limit:,.2f} \\\\
\\textbf{{Date}} & {datetime.now().strftime('%Y-%m-%d')} \\\\
\\end{{tabular}}

    \\section*{{Terms and Conditions}}
    Please review the terms and conditions associated with your credit card application.

\\end{{document}}
"""

    # Define the filenames
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    tex_filename = f"credit_card_application_{user_id}_{timestamp}.tex"
    pdf_filename = f"credit_card_application_{user_id}_{timestamp}.pdf"
    tex_filepath = os.path.join(APPLICATIONS_DIR, tex_filename)
    pdf_filepath = os.path.join(APPLICATIONS_DIR, pdf_filename)

    # Write LaTeX content to .tex file
    try:
        with open(tex_filepath, 'w') as file:
            file.write(latex_content)
        logging.info(f"Credit card application LaTeX file generated at {tex_filepath}.")
    except Exception as e:
        logging.error(f"Error writing LaTeX file: {e}")
        return Result(
            value="An error occurred while generating your credit card application. Please try again later.",
            agent=None
        )

    # Compile LaTeX to PDF using pdflatex
    try:
        subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filepath], check=True, cwd=APPLICATIONS_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.info(f"Credit card application PDF compiled at {pdf_filepath}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error compiling LaTeX to PDF: {e}")
        return Result(
            value="An error occurred while processing your credit card application. Please try again later.",
            agent=None
        )

    # Optionally, clean up the .aux and .log files generated by LaTeX
    for ext in ['.aux', '.log']:
        file_to_remove = os.path.join(APPLICATIONS_DIR, f"credit_card_application_{user_id}_{timestamp}{ext}")
        if os.path.exists(file_to_remove):
            os.remove(file_to_remove)

    # Upload the PDF to Pinata
    upload_pdf_to_pinata(pdf_filepath, "CARD")

    return Result(
        value=f"Your credit card application has been received and processed successfully. (File: {pdf_filename})",
        agent=None  # Transfer back to triage in AgentSwarm
    )
