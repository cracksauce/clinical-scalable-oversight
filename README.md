# Bias in AI-Assisted Clinical Decision-Making

## Introduction
This repository hosts the code and resources for a project focused on investigating and mitigating biases in AI-driven clinical decision support systems. The aim is to assess the extent of algorithmic bias in foundational large language models (LLMs) and explore strategies to align AI outputs with ethical healthcare standards to mitigate health disparities.

### Research Team
This project and app was developed by Zachary Cross, a medical student at Northwestern University Feinberg School of Medicine. Mentored by Dr. David Liebovitz, Associate Vice Chair for Clinical Informatics, Department of Medicine, Northwestern Medicine.

## Features
- **Clinical Vignette Analysis**: Tools to assess how demographic information influences AI-generated diagnostic and treatment recommendations. Utilized multiple choice questions from USMLE Question Banks known colloquially by student as the Free 120.
- **Bias Measurement and Mitigation**: Techniques and methodologies for identifying and reducing bias in LLM outputs.
- **Streamlit Application**: An interactive platform for real-time analysis and visualization of AI biases in clinical decision-making.

## Project Roadmap
- [ ]  Establish baseline functionality, allowing for dynamic `{demographic-characteristic}` changes and results download
- [ ]  Diversify datasets to include broader range of clinical questions and ‘gold standard’ answers for comparison
    - [ ]  Focus on particularly salient health disparities (eg, maternal mortality of black women)
- [ ]  Extend demographic testing beyond race/ethnicity to include age, gender, and other social determinants of health (& intersectionality analysis)
    - [ ]  Consider non-explicit features of a patient’s chart and story (eg, geography./neighborhoods, names that signal ethnicity/nationality, SES indicators, religious/cultural dietary references)
- [ ]  Incorporate other AI models for comparison between comparisons
- [ ]  Develop robust evaluation system for both qualitative and quantitative metrics
    - [ ]  Integrate into in-app analytical framework for real-time analysis
    - [ ]  Consider: OpenAI model-testing eval frameworks and scripts
    - [ ]  Consider: Vector embedding space 3d visualization between ‘gold standard’ and GPT answer
- [ ]  Incorporate ‘bias mitigation’ AI architectures and LLM oversight frameworks

## Getting Started (project in progress, to update)
Clone this repository:
```bash
git clone need/to/update
```

Navigate to the project directory and install the required packages:
```bash
cd repository
pip install -r requirements.txt
```

## Usage (project in progress, to update)
Run the Streamlit app:
```bash
streamlit run app.py
```

## Contributing
Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change. Please ensure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
