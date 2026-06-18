from transformers import pipeline
import random

MODEL_NAME = "google/flan-t5-small" # Very lightweight for CPU

_generator = None

def get_generator():
    global _generator
    if _generator is None:
        _generator = pipeline("text2text-generation", model=MODEL_NAME)
    return _generator

def extract_sentences(text, max_sentences=20):
    # Very rudimentary sentence extraction based on punctuation
    sentences = [s.strip() + "." for s in text.replace('!', '.').replace('?', '.').split('.') if len(s.strip()) > 30]
    # Randomly sample if too many
    if len(sentences) > max_sentences:
        sentences = random.sample(sentences, max_sentences)
    return sentences

def generate_flashcards(text, num_cards=5):
    """
    Generates Q&A flashcards using Flan-T5.
    """
    if not text:
        return []
        
    generator = get_generator()
    sentences = extract_sentences(text, num_cards + 5)
    
    flashcards = []
    for sentence in sentences[:num_cards]:
        # Generate a question from the sentence
        prompt = f"Generate a question based on this sentence: {sentence}"
        try:
            res = generator(prompt, max_length=50, do_sample=False)
            question = res[0]['generated_text']
            # We use the original sentence as the answer for simplicity and accuracy
            answer = sentence
            
            if question and question.lower() != sentence.lower():
                flashcards.append({
                    "question": question,
                    "answer": answer
                })
        except Exception as e:
            print(f"Flashcard generation error: {e}")
            
    # Fallback if generation failed
    if not flashcards:
        for sentence in sentences[:num_cards]:
            flashcards.append({
                "question": "What does the following statement refer to?\n" + sentence[:50] + "...",
                "answer": sentence
            })
            
    return flashcards

def generate_mcqs(text, num_mcqs=5):
    """
    Generates MCQs using the flashcard logic and creating distractors.
    """
    flashcards = generate_flashcards(text, num_cards=num_mcqs)
    
    # We will use other flashcard answers as distractors
    all_answers = [fc['answer'] for fc in flashcards]
    
    mcqs = []
    for i, fc in enumerate(flashcards):
        correct = fc['answer']
        # Get 3 other answers as distractors
        distractors = [a for j, a in enumerate(all_answers) if j != i]
        
        # If not enough distractors, generate dummy ones
        while len(distractors) < 3:
            distractors.append("All of the above.")
            distractors.append("None of the above.")
            distractors = list(set(distractors)) # Remove duplicates
            
        options = random.sample(distractors, min(3, len(distractors)))
        options.append(correct)
        random.shuffle(options) # Shuffle options
        
        mcqs.append({
            "question": fc['question'],
            "options": options,
            "correct": correct
        })
        
    return mcqs
