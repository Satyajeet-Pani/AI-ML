import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import pandas as pd
import uuid
import json
import os
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

class JobAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.setup_llm()
        
    def setup_llm(self):
        """Initialize the LLM with error handling"""
        try:
            self.llm = ChatGroq(
                temperature=0,
                groq_api_key="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",
                model_name="llama-3.3-70b-versatile"
            )
        except Exception as e:
            messagebox.showerror("LLM Error", f"Failed to initialize LLM: {str(e)}")
            self.llm = None
    
    def setup_ui(self):
        """Setup the user interface"""
        self.root.title("PrepMe")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Job Analyzer & Interview Prep Tool", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # URL Input Section
        url_frame = tk.LabelFrame(main_frame, text="Job Posting URL", 
                                 font=('Arial', 10, 'bold'), bg='#f0f0f0')
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.url_entry = tk.Entry(url_frame, width=100, font=('Arial', 10))
        self.url_entry.pack(padx=10, pady=10, fill=tk.X)
        
        # CSV File Section
        file_frame = tk.LabelFrame(main_frame, text="Portfolio CSV File", 
                                  font=('Arial', 10, 'bold'), bg='#f0f0f0')
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        file_input_frame = tk.Frame(file_frame, bg='#f0f0f0')
        file_input_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.file_entry = tk.Entry(file_input_frame, width=80, font=('Arial', 10))
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(file_input_frame, text="Browse", command=self.browse_file,
                              bg='#3498db', fg='white', font=('Arial', 9, 'bold'))
        browse_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Create sample CSV button
        sample_btn = tk.Button(file_input_frame, text="Create Sample CSV", 
                              command=self.create_sample_csv,
                              bg='#2ecc71', fg='white', font=('Arial', 9, 'bold'))
        sample_btn.pack(side=tk.RIGHT, padx=(5, 0))
        # Control buttons
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        self.analyze_btn = tk.Button(button_frame, text="🔍 Analyze Job", 
                                    command=self.run_analysis_threaded,
                                    bg='#e74c3c', fg='white', 
                                    font=('Arial', 12, 'bold'),
                                    padx=20, pady=5)
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="Clear Output", 
                             command=self.clear_output,
                             bg='#95a5a6', fg='white', 
                             font=('Arial', 10, 'bold'),
                             padx=15, pady=5)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Ready", 
                                    font=('Arial', 9), bg='#f0f0f0', fg='#7f8c8d')
        self.status_label.pack()
        
        # Output section
        output_frame = tk.LabelFrame(main_frame, text="Analysis Results", 
                                    font=('Arial', 10, 'bold'), bg='#f0f0f0')
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.output_box = scrolledtext.ScrolledText(output_frame, height=20, wrap=tk.WORD,
                                                   font=('Consolas', 9), bg='#2c3e50', fg='#ecf0f1')
        self.output_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        save_btn = tk.Button(output_frame, text="Save Results", 
                            command=self.save_results,
                            bg='#f39c12', fg='white', font=('Arial', 9, 'bold'))
        save_btn.pack(pady=(0, 10))

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Portfolio CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def create_sample_csv(self):
        sample_data = {
            'Technology': [
                'Python', 'JavaScript', 'React', 'Node.js', 'SQL', 'MongoDB',
                'Machine Learning', 'Data Analysis', 'AWS', 'Docker',
                'Git', 'REST APIs', 'HTML/CSS', 'TensorFlow', 'Pandas',
                'Flask', 'Django', 'PostgreSQL', 'Redis', 'Kubernetes'
            ],
            'Experience_Years': [
                '3', '2', '2', '1.5', '2.5', '1',
                '1.5', '2', '1', '1',
                '3', '2', '3', '1', '2',
                '2', '2.5', '3', '1', '0.5'
            ],
            'Projects_Count': [
                '5', '4', '3', '2', '6', '2',
                '3', '4', '2', '1',
                '10', '5', '8', '2', '4',
                '3', '4', '5', '2', '1'
            ],
            'Proficiency_Level': [
                'Advanced', 'Intermediate', 'Intermediate', 'Beginner', 'Advanced', 'Beginner',
                'Intermediate', 'Advanced', 'Beginner', 'Beginner',
                'Expert', 'Intermediate', 'Advanced', 'Beginner', 'Advanced',
                'Intermediate', 'Intermediate', 'Advanced', 'Beginner', 'Beginner'
            ]
        }

        try:
            file_path = filedialog.asksaveasfilename(
                title="Save Sample CSV",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")]
            )
            if file_path:
                df = pd.DataFrame(sample_data)
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Sample CSV created at:\n{file_path}")
                self.file_entry.delete(0, tk.END)
                self.file_entry.insert(0, file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create sample CSV: {str(e)}")
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def validate_url(self, url):
        try:
            response = requests.head(url, timeout=10)
            return response.status_code == 200
        except:
            return False

    def extract_job_data(self, url):
        try:
            options = EdgeOptions()
            options.use_chromium = True
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')

            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=options
            )
            driver.get(url)

            # Let page fully load (you can also use WebDriverWait if needed)
            driver.implicitly_wait(5)

            # Find all job links (this selector may need tweaking for your site)
            job_links = []
            elements = driver.find_elements("xpath", "//a[contains(@href, '/jobs/')]")
            for elem in elements:
                href = elem.get_attribute("href")
                if href and href.startswith("http") and href not in job_links:
                    job_links.append(href)

            print(f"Found {len(job_links)} job links.")

            # Visit each job detail page and collect job description text
            jobs = []
            for link in job_links[:5]:  # limit to 5 for testing
                try:
                    driver.get(link)
                    driver.implicitly_wait(3)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    job_text = soup.get_text(separator=' ', strip=True)
                    if len(job_text.split()) > 50:
                        jobs.append(job_text)
                except Exception as e:
                    print(f"⚠ Skipped {link}: {e}")

            driver.quit()

            print(f"Collected {len(jobs)} full job descriptions.")
            return jobs

        except Exception as e:
            raise Exception(f"Failed to scrape job listings: {str(e)}")

    def process_portfolio_simple(self, csv_path):
        try:
            df = pd.read_csv(csv_path)
            if 'Technology' not in df.columns:
                raise Exception("CSV must contain 'Technology' column")
            return df
        except Exception as e:
            raise Exception(f"Portfolio processing failed: {str(e)}")

    def generate_analysis(self, page_data, portfolio_df):
        if not self.llm:
            raise Exception("LLM not initialized")

        extract_prompt = PromptTemplate.from_template("""
        Analyze the following job posting and extract key information:

        {page_data}

        Extract and return ONLY a valid JSON object with these fields:
        {{
            "role": "job title",
            "company": "company name",
            "experience": "required experience",
            "skills": ["skill1", "skill2", "skill3"],
            "description": "brief job description",
            "requirements": ["req1", "req2", "req3"]
        }}
        Return only valid JSON, no additional text.
        """)

        extract_chain = extract_prompt | self.llm
        job_extract_result = extract_chain.invoke({'page_data': page_data[:4000]})
        job_data = JsonOutputParser().parse(job_extract_result.content)

        analysis_prompt = PromptTemplate.from_template("""
        Based on this job posting data: {job_data}
        And this portfolio: {portfolio_summary}

        Generate a comprehensive analysis as valid JSON:
        {{
            "skills_match": {{
                "matching_skills": ["skill1", "skill2"],
                "missing_skills": ["skill3", "skill4"],
                "match_percentage": 75
            }},
            "interview_questions": [
                {{
                    "category": "Technical",
                    "question": "Technical question here",
                    "focus_area": "specific skill"
                }},
                {{
                    "category": "Behavioral",
                    "question": "Behavioral question here", 
                    "focus_area": "soft skill"
                }}
            ],
            "preparation_tips": [
                "tip1 based on missing skills",
                "tip2 for interview success"
            ]
        }}
        Generate as many diverse interview questions as possible (but less thatn 20) covering technical, behavioral, and role-specific areas.
        Return only valid JSON.
        """)

        portfolio_summary = portfolio_df['Technology'].tolist()[:20]
        analysis_chain = analysis_prompt | self.llm
        analysis_result = analysis_chain.invoke({
            'job_data': json.dumps(job_data),
            'portfolio_summary': str(portfolio_summary)
        })

        analysis_data = JsonOutputParser().parse(analysis_result.content)

        return {
            'job_posting': job_data,
            'analysis': analysis_data,
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def preprocess_job_posting(self, url, portfolio_csv_path):
        self.update_status("Validating URL...")
        if not self.validate_url(url):
            raise Exception("Invalid or inaccessible URL")

        self.update_status("Extracting job data...")
        job_texts = self.extract_job_data(url)

        self.update_status("Processing portfolio...")
        portfolio_df = self.process_portfolio_simple(portfolio_csv_path)
        results = []

        for job_text in job_texts:
            try:
                result = self.generate_analysis(job_text, portfolio_df)
                results.append(result)
            except Exception as e:
                print(f"Skipping job due to error: {e}")

        self.update_status("Analysis complete!")
        return results
    def run_analysis_threaded(self):
        def analysis_thread():
            try:
                self.analyze_btn.config(state='disabled')
                self.progress.start()

                url = self.url_entry.get().strip()
                file_path = self.file_entry.get().strip()

                if not url or not file_path:
                    messagebox.showerror("Missing Input", "Provide both URL and CSV file.")
                    return

                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url

                if not os.path.exists(file_path):
                    messagebox.showerror("File Error", f"CSV file not found: {file_path}")
                    return

                results = self.preprocess_job_posting(url, file_path)
                self.output_box.delete(1.0, tk.END)

                formatted_all = []
                for i, result in enumerate(results, 1):
                    formatted = self.format_output(result)
                    formatted_all.append(f"\n\n🔹 JOB #{i}\n" + formatted)

                self.output_box.insert(tk.END, "\n".join(formatted_all))
                self.last_result = results
                messagebox.showinfo("Success", "Analysis completed!")

            except Exception as e:
                self.output_box.delete(1.0, tk.END)
                self.output_box.insert(tk.END, f"ERROR: {e}")
                messagebox.showerror("Error", str(e))

            finally:
                self.progress.stop()
                self.analyze_btn.config(state='normal')
                self.update_status("Ready")

        threading.Thread(target=analysis_thread, daemon=True).start()

    def format_output(self, result):
        output = []
        output.append("=" * 80)
        output.append("JOB ANALYSIS RESULTS")
        output.append("=" * 80)
        output.append("")

        job_info = result.get('job_posting', {})
        output.append("JOB POSTING DETAILS:")
        output.append("-" * 30)
        output.append(f"Role: {job_info.get('role', 'N/A')}")
        output.append(f"Company: {job_info.get('company', 'N/A')}")
        output.append(f"Experience: {job_info.get('experience', 'N/A')}")
        output.append("")

        analysis = result.get('analysis', {})
        skills_match = analysis.get('skills_match', {})
        output.append("SKILLS ANALYSIS:")
        output.append("-" * 30)
        output.append(f"Match Percentage: {skills_match.get('match_percentage', 'N/A')}%")

        matching = skills_match.get('matching_skills', [])
        if matching:
            output.append(f"✅ Matching Skills: {', '.join(matching)}")

        missing = skills_match.get('missing_skills', [])
        if missing:
            output.append(f" Missing Skills: {', '.join(missing)}")
        output.append("")

        questions = analysis.get('interview_questions', [])
        if questions:
            output.append("INTERVIEW QUESTIONS:")
            output.append("-" * 30)
            for i, q in enumerate(questions, 1):
                output.append(f"{i}. [{q.get('category', 'General')}] {q.get('question', 'N/A')}")
                if q.get('focus_area'):
                    output.append(f"   Focus: {q['focus_area']}")
                output.append("")

        tips = analysis.get('preparation_tips', [])
        if tips:
            output.append("PREPARATION TIPS:")
            output.append("-" * 30)
            for i, tip in enumerate(tips, 1):
                output.append(f"{i}. {tip}")
            output.append("")

        output.append("=" * 80)
        output.append(f"Generated on: {result.get('timestamp', 'N/A')}")
        output.append("=" * 80)

        return "\n".join(output)

    def clear_output(self):
        self.output_box.delete(1.0, tk.END)
        self.update_status("Output cleared")

    def save_results(self):
        if not hasattr(self, 'last_result'):
            messagebox.showwarning("No Results", "No analysis results to save.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Analysis Results",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                if file_path.endswith('.json'):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        if isinstance(self.last_result, list):
                            json.dump(self.last_result, f, indent=2)
                        else:
                            json.dump([self.last_result], f, indent=2)
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(self.format_output(self.last_result))
                messagebox.showinfo("Success", f"Saved to: {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

def main():
    root = tk.Tk()
    app = JobAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
