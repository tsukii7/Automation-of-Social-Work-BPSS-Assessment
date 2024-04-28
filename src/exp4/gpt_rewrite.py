import os

from openai import OpenAI

from src.exp2.util import rewrite_prompt

os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI()

system_message = {
    "role": "system",
    "content": rewrite_prompt
}
def transform_dialogue_to_narrative(dialogue):
    dialogue_string = "\n".join(dialogue)
    print(dialogue_string)

    user_message = "Here is the dialogue: \n" + dialogue_string

    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=0.1,
        messages=[
            system_message,
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return completion.choices[0].message.content


# Example usage
dialogue = """
"u: Hello is this the right place to come if I have some emotional issues?",
"a: Yes, you're in the right place. How can I assist you today?",
"u: I haven't been feeling myself lately and worry that something is wrong",
"a: I'm sorry to hear that you're feeling this way. Can you share more about what's been going on?",
"u: I have been having mood swings and get angry with my friends/ mum easily",
"a: It sounds like these mood swings are impacting your relationships. Have there been any recent changes or stressors in your life? ",
"a:  It's important to understand what might be triggering these feelings.",
"u: I don't think so",
"a: Sometimes, triggers aren't immediately obvious. It might help to reflect on any subtle changes or stress. ",
"a:  Would you like to talk about how these mood swings and anger make you feel?",
"u: I don't know who I am anymore",
"u: I have been feeling very tired",
"u: and no mood to do any of my homework",
"u: some days I skip meals as I just don't feel hungry",
"a: I'm sorry you're facing these difficulties. Let's try to understand a bit more about how you've been feeling lately so I can better help you. ",
"a:  I'm going to ask you a series of questions about your feelings in the past four weeks. Just answer as honestly as you can, okay? ",
"a:  In the past four weeks, how often have you felt tired out for no good reason? The options for responding are 'none, a little, some, most or all of the time'.",
"u: most of the time",
"a: I'm sorry to hear that. It must be tough. ",
"a:  Next, in the past four weeks, how often have you felt nervous?",
"u: just a little",
"a: Thanks for sharing. ",
"a:  Next, in the past four weeks, how often have you felt so nervous that nothing could calm you down?",
"u: I don't feel this way",
"a: That's good to hear. ",
"a:  Next, in the past four weeks, how often have you felt hopeless?",
"u: all of the time",
"a: I'm really sorry to hear that. It sounds incredibly challenging. ",
"u: yes it is"
"""

narrative = transform_dialogue_to_narrative(dialogue)
print(narrative)
