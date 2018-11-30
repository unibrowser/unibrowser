# Prachi S. Rahurkar - 
# Contains the function_to find nouns in a query fired by the user

import nltk
#nltk.download('averaged_perceptron_tagger')

def find_nouns_in_query():

    lines_array = ['Do I have to add another year to my studies if I want to study abroad?', 'Do I have to study abroad in Engineering?',
                   'Where will I be living?', 'I dont want to study Engineering in another language can I still go abroad?', 'Isnt study abroad really expensive?',
                   'Will I be able to get the courses I need if I study abroad?',
                   'I am planning to take a certain group of courses my department recommends for a certain term, will I be able to get these courses abroad?',
                   'Can I go abroad with my friend who isnt an engineering major?', 'Am I required to live on campus?',
                   'I dont know if Ive been admitted to Oregon State yet. Can I still apply for Housing?', 'How do I start the application process?',
                   'I am the parent of a student coming to Oregon State. Can I apply for housing for them?', 'What does submission of a housing application do?',
                   'Will I need to pay a deposit or advance rent payment?', 'What if I am admitted to the University late?',
                   'What is the housing contract?', 'Do I have to sign my contract by a certain time?', 'How long is the contract valid?',
                   'Should I still sign my contract, even if I want to change my room?', 'What if I am leaving OSU or moving off-campus in the middle of the year?',
                   'What will my contract cancellation fee be?', 'If I want to move to a different room do I need to sign another contract?',
                   'What if I want to join a sorority or fraternity?', 'Do I have to have a dining plan while living on campus?', 'Where can I use my dining plan?',
                   'How do I change my dining plan?', 'What is Orange Rewards?', 'When do classes start? When can I move in?',
                   'Do I have to move in the day my residence hall opens?', 'Can I check-in early?', 'Where do I go to pick up my room key(s)?',
                   'What if I am not going to be moving in on move-in day?', 'What appliances are allowed in my room?', 'What items are prohibited?',
                   'Am I allowed to bring any sort of animals/pets into my room?', 'How do I set up the internet in my room?', 'I want to move out. How do I do this?',
                   'Can I move somewhere else on campus?', 'What if I moved out of my room without telling my Resident Director (RD) or Area Director (AD)?',
                   'What does a clean room entail?', 'What happens to my mail when I move out?', 'What if I want to appeal any of the charges UHDS has put onto my account after my moving out?',
                   'My roommate moved out; can I spread out my personal belongings since I am the only one living there?',
                   'I am moving onto campus during the middle of the academic year. How long will my contract be for?', 'What if I need emergency housing?',
                   'I want to apply for housing during the middle of a term/year. Which housing application do I need to fill out?',
                   'If I move onto campus during the middle of a term is my room rate pro-rated?', 'What is INTO OSU?', 'Where do INTO OSU students stay on campus?', 'Can I live with an INTO OSU student?',
                   'My room is currently half open; will I be receiving an international roommate?', 'What if I cant find my food?', 'Im an international student, when can I move in?',
                   'As an international student, will my appliances work?', 'What if I dont get along with my roommate?', 'What if I want to live in a housed sorority or fraternity?', 'Can I live with my friend?',
                   'What if I have a specific medical condition that requires me to live in a certain environment?',
                   'Can my therapy/service animal stay with me in my room?',
                   'What if my room was deemed not ready to accept a new roommate and my rate was changed?', 'Are the residence halls co-ed? Are there any single-gender options?',
                   'I prefer to live in a substance-free community. What options are there?',
                   'How do I submit a maintenance request?', 'How do I update my contact information?', 'How do I reserve a loft or bunk kit?',
                   'How do I make a disability and dietary accommodation request?', 'What if I believe I have been wrongly charged regarding a charge from University Housing and Dining Services?', 'What is my address while I live on campus?',
                   'Are the rooms furnished?', 'How do I make a counseling appointment?', 'What are the drop-in hours?', 'What group therapy options are available?',
                   'When are Mindfulness Meditation drop-ins offered?', 'What is the process for Emotional Support or Assistance Animals?', 'Where can I find information on upcoming CAPS events?',
                   'What do I do if I need to talk to someone when CAPS is closed?', 'What if I dont click with my counselor and want to request to change counselors?']

    i = 0

    for i in range(len(lines_array)):
        # function to test if something is a noun
        is_noun = lambda pos: pos[:2] == 'NN'

        # do the nlp stuff
        tokenized = nltk.word_tokenize(lines_array[i])
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 

        print(nouns)


if __name__ == '__main__':
    
    noun_phrases = ["smelly cats","pink cats","funny dogs","natural language processing","computer processing"]
    is_noun = lambda pos: pos[:2] == 'NN'
    # do the nlp stuff
    tokenized = nltk.word_tokenize(lines_array[i])
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
    if nouns != 0:
        find_nouns_in_query()