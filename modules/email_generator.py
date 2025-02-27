from langchain_core.prompts import PromptTemplate

def generate_email(job_info, portfolio_links, user_name, llm, config):
    """
    Generate a cold email based on job info, portfolio, and configuration.
    """
    # Format links for the prompt with titles
    link_list = [f"[{link_data['title']}]({link_data['links']})" for link_data in portfolio_links if link_data and 'links' in link_data]

    # Create a compelling prompt for email generation
    prompt_email = PromptTemplate.from_template(
        """
        ### INFORMATION:
        {job_description}

        ### INSTRUCTION:
        You are {name}, a {position} at {company_name}. {company_name} is a leading company dedicated to {company_description}.
        Your goal is to craft a persuasive cold email regarding {email_purpose}, showcasing {company_name}'s capabilities and your personal strengths.
        Highlight how {company_name} can uniquely meet the recipient's needs and exceed their expectations.
        Include relevant links from your portfolio to demonstrate past successes and expertise: {link_list}.
        Use a confident and enthusiastic tone to convey your eagerness to collaborate and the value you can bring.
        Write a compelling subject line that grabs attention and increases open rates.
        The email should be professional yet engaging, with short, concise paragraphs for readability.
        Include a clear and compelling call to action, encouraging the recipient to take the next step.
        Do not provide a preamble.

        ### EMAIL (NO PREAMBLE):
        Subject: [Insert Compelling Subject Line Here]

        Hi [Recipient's Name],

        I hope this email finds you well. I came across [mention how you found them] and was impressed by [specific aspect of their work or company].
        I believe {company_name} can offer unique solutions tailored to your needs, particularly in [specific area related to job_description].

        At {company_name}, we specialize in {company_description}. Our approach is not just about delivering services but about building lasting partnerships that drive success.
        With a proven track record in [mention relevant skills or industries], we are confident in our ability to exceed your expectations.

        I invite you to explore some of our past projects and success stories:
        {link_list}

        I would love the opportunity to discuss how we can collaborate and achieve great results together. Please let me know if you're available for a quick chat sometime next week.

        Looking forward to the possibility of working together.

        Best regards,
        {name}
        {position} at {company_name}
        [Your Contact Information]
        """
    )

    # Generate email
    chain_email = prompt_email | llm
    res = chain_email.invoke({
        "job_description": str(job_info),
        "link_list": " ".join(link_list),  # Ensure link_list is a single string with clickable links
        "name": user_name,
        "position": config['position'],
        "company_name": config['company_name'],
        "company_description": config['company_description'],
        "email_purpose": config['email_purpose']
    })

    return res.content
