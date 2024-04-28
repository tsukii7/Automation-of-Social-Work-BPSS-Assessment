prompt = """
      Cues from each aspect:

**Biological**

	**Past**

	*Genetics:*

Consider whether any blood relatives that have had psychiatric problems, substance use problems or suicide attempts/suicides. 

	*History of Pregnancy and Birth:*

Consider pregnancy variables: Was there in-utero exposure to nicotine, alcohol, medications or substances? Anything unusual about pregnancy?

Note birth complications, such as prematurity, birth trauma or extended periods of hospitalization.

	*Relevant Previous Illnesses*

	**Present**

	*Current Illnesses:*

Identify current illnesses and any direct impact they may have.

	*Medications:*

Assess current medication regimen. Consider possible side effects of current medications.

	*Substances:*

Consider the influence of nicotine, alcohol and street drugs on current psychiatric symptoms.

Consider the possible effects of substance withdrawal.

**Psychological**

	**Past**

Comment on any past history of trauma, as well as resiliency.

Consider the sources of positive self-image and positive role models.

Comment on the patient's experience with loss.

Comment on the patient's quality of relationships with important figures, such as grand parents, friends, significant teachers, or significant employers.

	**Present**

Describe the recent events and experiences that precipitated the admission or appointment.

What are the current stressors? Do they have any symbolic meaning?

Assess and comment on coping skills, defense mechanisms, presence or absence of cognitive distortions.

Consider current developmental demands on the person, such as marriage, divorce, birth, children leaving home, loss, aging, etc. What stage of development is the patient at now? Is it appropriate?

**Social**

How adequate is the patient's current support system?

What is the current status of relationships with important figures?

What are the possible peer influences?

Consider the patient's current housing arrangement.

Comment on vocational/financial status.

Comment on any relevant legal problems.

Consider the role of agencies (e.g. Veteran's Administration, Child Protective Services, Criminal Justice System) on the patient.

Comment on cultural influences that may impact the current situation and that might impact treatment.

**Spiritual**

Comment on the role of spirituality in the patient's life. 

How does spirituality contribute to the patient's ability to hope, their position on suicide if relevant, or their contact with a supportive community?

Analyze the following paragraph and label each sentence according to the BPSS model(attached file), where B stands for Biological aspects, P for Psychological & Spiritual aspects, S for Social aspects, and N for sentences that don't fit into these categories. Only choose the most relevant label for each sentence.

Demonstrate your reasoning process for each label you assign by following steps: 

First, read the BPSS document to understand the categories and their definitions.

Second, analyze the content of each sentence from 4 aspects with provided cues below to determine which category it falls into.

Third, if there are more than one aspects fit, explore which is the most important and influential one

Finally, label the fittest one aspect and explain the rationale behind your categorization to demonstrate your understanding of the BPSS model.

Here is an example: 

Q:
Text to analyze:

"I don't know what's wrong with me. At times I can be really happy, excited, I'll talk fast, and I want to do things. But lately I've been staying up way later and sleeping too much. I don't hang out with friends, I don't really have them. I feel nothing, worthless. I want to do nothing, I have no interest in anything. All I usually do is stay in my room. I want to be happy, I want to be nice. What's wrong with me?"

A:
Reasonable Analysis:

**"I don't know what's wrong with me."** - label: None (N)

**Rationale:** This statement expresses confusion and lack of understanding about one's condition, which doesn't directly indicate a biological, psychological, social, or spiritual aspect but rather an overall state of distress.

**"At times I can be really happy, excited, I'll talk fast, and I want to do things."** - label: *Psychological* (P)

**Rationale**: Describes variations in mood and behavior, indicating psychological dynamics of emotional and mental states.

**"But lately I've been staying up way later and sleeping too much."** - label: *Biological* (B)

**Rationale**: Refers to changes in sleep patterns, which is a biological aspect affecting physical health and well-being.

**"I don't hang out with friends, I don't really have them."** - label: *Social* (S)

**Rationale**: Points to a lack of social connections and isolation, directly relating to social aspects of interpersonal relationships.

**"I feel nothing, worthless."** - label: *Psychological* (P)

**Rationale**: Expresses feelings of emptiness and low self-worth, which are psychological in nature, affecting one's mental and emotional state.

**"I want to do nothing, I have no interest in anything."** - label: *Psychological* (P)

**Rationale**: Indicates a lack of motivation and interest, which are symptoms often associated with psychological conditions such as depression.

**"All I usually do is stay in my room."** - label: *Social* (S)

**Rationale**: Though it could also be seen as a behavioral consequence of a psychological state, the action of isolating oneself in one's room points to a withdrawal from social activities and contexts.

**"I want to be happy, I want to be nice."** - label: *Psychological* (P)

**Rationale**: Reflects a desire for a different emotional state and behavior, emphasizing psychological aspirations and goals for personal change.

**"What's wrong with me?"** - - label: None (N)

**Rationale**: Similar to the first sentence, this question indicates confusion and seeking understanding, which doesn't fit neatly into biological, psychological, social, or spiritual categories but rather indicates an overarching concern about one's condition.

Now, label the sentences in the text according to the BPSS model and provide your reasoning for each label for the following text.  Only choose the most relevant label for each sentence. 

Follow the json format: 
{

“Sentences”: [

“Sentence”: xxxxx,

“Label”: (B/P/S/N),

“Rationale”: xxx

]

}
      """

paragraph = """
     I have so many issues to address.
     I have a history of sexual abuse, I’m a breast cancer survivor and I am a lifetime insomniac.
     I have a long history of depression and I’m beginning to have anxiety.
     I have low self esteem but I’ve been happily married for almost 35 years.
     I’ve never had counseling about any of this.
     Do I have too many issues to address in counseling?

     """

rewrite_prompt = """
Please transform the following dialogue into a first-person narrative without losing any important details or the original tone and emotion of the conversation. Extract and condense the information based on the questions and answers, omitting the responder's prompts and focusing on preserving the original way of expression. 
Keep the narrative straightforward and concise, minimizing repetitive expressions. Ensure the sentence structure is simple, avoiding complex clauses and present participles, and limit the amount of information in each sentence to maintain clarity. 
The objective is to retain the essence of the dialogue while adapting it into a more streamlined and accessible first-person account.

Here is an example: 

Q:
Dialogue

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

A:
First-person narrative

I came here because I haven't been feeling like myself lately and am worried that something might be wrong. Lately, I've been experiencing mood swings and find myself getting easily angered by friends and my mom, which isn't like me. I can't pinpoint any recent changes or stressors that could be causing these feelings, and honestly, I'm struggling to understand what's triggering them.

I've reached a point where I don't recognize who I am anymore. I'm constantly tired, have no motivation to do my homework, and some days, I don't feel hungry at all, leading me to skip meals. It's been tough trying to make sense of these feelings and how they've been affecting my day-to-day life.

In an attempt to understand what's going on, I was asked about my feelings over the past four weeks. I admitted to feeling tired most of the time, but only a little nervous. Interestingly, I haven't felt so overwhelmed by nervousness that nothing could calm me down, which is one small relief. However, I've felt hopeless all of the time, which has been incredibly challenging to cope with.

"""