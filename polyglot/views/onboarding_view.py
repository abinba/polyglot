import customtkinter as ctk
from typing import List, Callable
from polyglot.controllers.user_controller import UserController
from polyglot.controllers.vocabulary_controller import VocabularyController

class OnboardingView(ctk.CTkFrame):
    def __init__(self, parent, user_controller: UserController,
                 vocab_controller: VocabularyController,
                 on_complete: Callable):
        super().__init__(parent)
        self.user_controller = user_controller
        self.vocab_controller = vocab_controller
        self.on_complete = on_complete
        
        self.current_step = 0
        self.user_data = {
            'native_language': '',
            'target_language': '',
            'level': '',
            'topics': [],
            'include_phrases': True
        }
        
        # Available options
        self.languages = ["English", "Spanish", "French", "German",
                         "Italian", "Portuguese", "Russian", "Chinese",
                         "Japanese", "Korean"]
        self.levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
        self.topics = ["Business", "Travel", "Technology", "Culture",
                      "Food", "Sports", "Education", "Entertainment",
                      "Science", "Nature"]
        
        self.setup_ui()
        self.show_step(0)
    
    def setup_ui(self):
        """Set up the main UI components"""
        # Title
        self.title = ctk.CTkLabel(
            self,
            text="Welcome to Polyglot!",
            font=("Helvetica", 24, "bold")
        )
        self.title.pack(pady=20)
        
        # Content frame
        self.content = ctk.CTkFrame(self)
        self.content.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Navigation buttons
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(pady=20, fill="x")
        
        self.prev_btn = ctk.CTkButton(
            self.nav_frame,
            text="Previous",
            command=self.prev_step
        )
        self.prev_btn.pack(side="left", padx=20)
        
        self.next_btn = ctk.CTkButton(
            self.nav_frame,
            text="Next",
            command=self.next_step
        )
        self.next_btn.pack(side="right", padx=20)
    
    def show_step(self, step: int):
        """Show the specified onboarding step"""
        # Clear previous content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        if step == 0:
            self.show_language_selection("native")
        elif step == 1:
            self.show_language_selection("target")
        elif step == 2:
            self.show_level_selection()
        elif step == 3:
            self.show_topic_selection()
        elif step == 4:
            self.show_phrases_selection()
        
        # Update navigation buttons
        self.prev_btn.configure(state="normal" if step > 0 else "disabled")
        self.next_btn.configure(
            text="Finish" if step == 4 else "Next"
        )
    
    def show_language_selection(self, lang_type: str):
        """Show language selection step"""
        label = ctk.CTkLabel(
            self.content,
            text=f"Select your {'native' if lang_type == 'native' else 'target'} language:",
            font=("Helvetica", 16)
        )
        label.pack(pady=10)
        
        for lang in self.languages:
            btn = ctk.CTkButton(
                self.content,
                text=lang,
                command=lambda l=lang: self.select_language(lang_type, l)
            )
            btn.pack(pady=5)
            
            # Highlight selected language
            if self.user_data[f'{lang_type}_language'] == lang:
                btn.configure(fg_color="green")
    
    def show_level_selection(self):
        """Show language level selection step"""
        label = ctk.CTkLabel(
            self.content,
            text="Select your proficiency level:",
            font=("Helvetica", 16)
        )
        label.pack(pady=10)
        
        for level in self.levels:
            btn = ctk.CTkButton(
                self.content,
                text=level,
                command=lambda l=level: self.select_level(l)
            )
            btn.pack(pady=5)
            
            if self.user_data['level'] == level:
                btn.configure(fg_color="green")
    
    def show_topic_selection(self):
        """Show topic selection step"""
        label = ctk.CTkLabel(
            self.content,
            text="Select topics you're interested in (multiple choice):",
            font=("Helvetica", 16)
        )
        label.pack(pady=10)
        
        for topic in self.topics:
            var = ctk.StringVar(value="0")
            cb = ctk.CTkCheckBox(
                self.content,
                text=topic,
                variable=var,
                command=lambda t=topic, v=var: self.toggle_topic(t)
            )
            cb.pack(pady=5)
            
            if topic in self.user_data['topics']:
                cb.select()
    
    def show_phrases_selection(self):
        """Show phrases inclusion selection step"""
        label = ctk.CTkLabel(
            self.content,
            text="Would you like to include common phrases?",
            font=("Helvetica", 16)
        )
        label.pack(pady=10)
        
        var = ctk.StringVar(value="1" if self.user_data['include_phrases'] else "0")
        cb = ctk.CTkCheckBox(
            self.content,
            text="Include phrases",
            variable=var,
            command=lambda: self.toggle_phrases(var.get() == "1")
        )
        cb.pack(pady=5)
    
    def select_language(self, lang_type: str, language: str):
        """Handle language selection"""
        self.user_data[f'{lang_type}_language'] = language
        self.show_step(self.current_step)
    
    def select_level(self, level: str):
        """Handle level selection"""
        self.user_data['level'] = level
        self.show_step(self.current_step)
    
    def toggle_topic(self, topic: str):
        """Handle topic selection/deselection"""
        if topic in self.user_data['topics']:
            self.user_data['topics'].remove(topic)
        else:
            self.user_data['topics'].append(topic)
    
    def toggle_phrases(self, include: bool):
        """Handle phrases inclusion toggle"""
        self.user_data['include_phrases'] = include
    
    def prev_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step(self.current_step)
    
    def next_step(self):
        """Go to next step or finish onboarding"""
        if self.current_step < 4:
            self.current_step += 1
            self.show_step(self.current_step)
        else:
            self.finish_onboarding()
    
    def finish_onboarding(self):
        """Complete onboarding and generate initial vocabulary"""
        # Save user settings
        self.user_controller.create_user(
            native_lang=self.user_data['native_language'],
            target_lang=self.user_data['target_language'],
            level=self.user_data['level'],
            topics=self.user_data['topics'],
            include_phrases=self.user_data['include_phrases']
        )
        
        # Generate initial vocabulary
        words = self.vocab_controller.generate_words(
            native_lang=self.user_data['native_language'],
            target_lang=self.user_data['target_language'],
            level=self.user_data['level'],
            topics=self.user_data['topics'],
            include_phrases=self.user_data['include_phrases']
        )
        
        # Add words to vocabulary
        self.vocab_controller.add_words(words)
        
        # Complete onboarding
        self.on_complete()
