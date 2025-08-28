class Prompts:
    analysis_prompt = """
    Input Data: {raw_text_data}

    Instructions:
        - Carefully analyze the context of the information in above raw text.
        - Extract the key information from the page in extreme detail.
        - If no information is available, return an empty json object.
        - Do not include placeholders or hallucinate information.
        - Output the information in a structured json format.
        - Ensure the output is a valid, error-free JSON object with all fields correctly formatted.
        - You must not use any null values in the output.
        - Use relevant keys and values from the document to structure the output.
        - Always complete the json output, don't return partial json.
    """

    summarize_prompt = """
    Input Data: {text}
    Instructions:
        - Carefully analyze the context of the information in above raw text.
        - The text is extracted with OCR, hence may contain errors or jumbled words.
        - Summarize the content clearly and concisely, using natural language.
        - Talk about the information without referring to the text or document directly.
        - Stick to key information, avoid repetition/conflicts and use chronological order wherever necessary..
        - Your response must not contain any formatting, headings, or bullet points such as
        - 'Here's a summary of the page:'.\n Do not hallucinate or make up information.
    """