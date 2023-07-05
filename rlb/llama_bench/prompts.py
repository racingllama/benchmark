"""Generate multiple promps for testing."""


def prompts():
    """Generate a prompt."""
    prompts = [
        "test",
        "What is the meaning of life?",
        "What is the airspeed velocity of an unladen swallow?",
        "What is the capital of Vermont?",
        "Create a python function that returns a list of files in a directory recursively. Include subdirectories.",
        "Create a python function that returns a list of files in a directory using a single function. Include subdirectories.",
        "Create a go program that implements a simple web server that returns a list of files in a directory recursively. Include subdirectories.",
        "Generate a list of ten titles for my next blog post. The topic is 'Machine Learning using Python'. The titles should be unique and not contain any stop words.",
        "Generate a list of ten titles for my next blog post. The topic is 'Machine Learning using Python'. The titles should be unique and not contain any stop words. The titles should be in the form of a question.",
        "Generate a list of ten titles for my next blog post. The topic is 'Machine Learning using Python'. The titles should be unique and not contain any stop words. The titles should be in the form of a question. The titles should be at least 10 words long.",
        "Generate a list of ten titles for my next blog post. The topic is 'Machine Learning using Python'. The titles should be unique and not contain any stop words. The titles should be in the form of a question. The titles should be at least 10 words long. The titles should be at least 50 characters long.",
        "Generate a list of ten titles for my next blog post. The topic is 'Machine Learning using Python'. The titles should be unique and not contain any stop words. The titles should be in the form of a question. The titles should be at least 10 words long. The titles should be at least 50 characters long. The titles should be in title case.",
        "Write a blog post for me. The topic is 'Machine Learning using Python'. The post should be at least 500 words long.",
        "Write a tweet for me. The topic is 'Machine Learning using Python'. The tweet should be at least 120 characters long.",
        "Expand on the following bullet points: 1. Cooking with fire is a fun thing to do 2. I like to cook with fire 3. I refuse to eat raw food",
        "How do I cook a steak without a grill? I don't have a grill. I don't want a grill. I don't like grills. My HOA Hates grills. They'll kick me out of my house if I use one. I don't want to be homeless, but I do want steak. How do I do this without getting thrown out.",
        "Write a short story that includes 3 characters, a setting, and a plot. The story should be at least 500 words long. It needs to be set in a futuristic world that feels like an old western movie. It takes place in an old mining town. The town has seen better days. Most people have left, but there's still a few who call it home and refuse to leave. The scene should open in a bar. The bar looks like it came out of a cyberpunk novel. There's people milling about and a robot is in the background playing chess against an empty chair. The lights flicker. Why do they flicker?",
        "Feedback? I'm looking for feedback on my latest blog post. It's about how to write a blog post using LLM completion. Do you know what this is? Well, back in my day we didn't get feedback. or LLMs. or computers. All we had was a hat. and we liked it. It was a nice hat. But we only had one. We shared it. I got it every other Tuesday. That was my hat day.",
        "What is the meaning of life? I've been thinking about this a lot lately. I think it's to be happy. But what does that mean? I don't know. I'm not happy. I'm sad. I'm lonely. I'm depressed. I'm anxious. I'm scared. I'm angry. I'm frustrated. I'm tired",
        "I answered the phone. It was another scam.",
        "Why should you have all the fun?",
    ]
    while True:
        for prompt in prompts:
            yield prompt
