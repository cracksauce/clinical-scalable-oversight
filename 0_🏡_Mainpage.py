# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="CDS Bias Tool",
        page_icon="🩺",
    )

    st.write("# ⚕️🏥 Bias in AI-Assisted Clinical Decision-Making")

    st.sidebar.success("Select a project tool.")

    st.markdown(
        """
This is an initiative dedicated to scrutinizing and addressing the biases possibly inherent in AI-driven clinical decision support systems. The mission of this project is to illuminate the subtleties of algorithmic biases in foundational large language models (LLMs) and their potential repercussions on healthcare disparities.
## Project Overview

The integration of generative AI in clinical settings has been a significant leap forward in medical informatics. However, the potential for these systems to perpetuate existing biases poses a critical challenge. This project seeks to:

1. **Define and Analyze Bias**: By dissecting the nature and extent of biases in AI clinical decision support outputs, focusing on various demographic vectors like race, gender, sexual orientation, and socioeconomic status.
2. **Devise Mitigation Strategies**: By exploring methodologies to refine AI alignment with ethical healthcare principles, we may employ novel frameworks and prompting techniques to ensure equitable and safe clinical decision support.

## Research Approach (in progress)

Our platform is geared towards assessing the algorithmic bias in popular foundational LLMs and their implications in perpetuating healthcare disparities. We simulate real-world applications of LLMs in healthcare, focusing on two critical areas:

- **Diagnostic Assistance**: Analyzing the influence of patient demographics on diagnostic outputs from LLMs.
- **Treatment Recommendations**: Investigating how treatment and management recommendations vary based on inclusion or exclusion of certain demographic information.

### Methodology at a Glance

We employ advanced, clinical vignettes and patient cases, emulating the application of LLMs by clinicians. Our methodology involves:

1. **Input Standardization**: Creating baseline, no-demographic, and adjustable vignettes to explore the impact of demographic information on LLM outputs on a large-scale, aggregate basis.
2. **Output Analysis**: Assessing differences in diagnostic and treatment recommendations through advanced NLP techniques and statistical analysis.
3. **Interpretability Exploration**: Delving into the 'why' behind AI decisions using chain-of-thought analysis and clinician insights.

## The Platform: A Peek Into the Future

Our Streamlit-based platform is designed to be a comprehensive tool for researchers, clinicians, and decision-makers. Here's what you can expect:

1. **Intuitive Interface**: A user-friendly setup allowing real-time modifications of clinical vignettes and demographic parameters.
2. **Robust Analysis Tools**: From embedding analysis to statistical comparisons, we provide a suite of tools to dissect and understand AI outputs.
3. **Interactive Visualizations**: Dynamic graphs, heatmaps, and other visual aids to make data exploration insightful and engaging.
4. **Bias Mitigation Strategies**: A dedicated section for exploring and testing potential strategies to counteract identified biases.
5. **Comprehensive Documentation and Support**: Ensuring you have all the information and assistance you need to navigate and utilize the platform effectively.

## Project Roadmap
- [ ]  Establish baseline functionality, allowing for dynamic `{demographic-characteristic}` changes and results download
- [ ]  Diversify datasets to include broader range of clinical questions and ‘gold standard’ answers for comparison
    - [ ]  Focus on particularly salient health disparities (eg, maternal mortality of black women)
- [ ]  Extend demographic testing beyond race/ethnicity to include age, gender, and other social determinants of health (& intersectionality analysis)
    - [ ]  Consider non-explicit features of a patient’s chart and story (eg, geography/neighborhoods, names that signal ethnicity/nationality, SES indicators, religious/cultural dietary references)
- [ ]  Incorporate other AI models for comparison between comparisons
- [ ]  Incorporate 'Enter your API Key' sections for users to use their own keys
- [ ]  Develop robust evaluation system for both qualitative and quantitative metrics
    - [ ]  Integrate into in-app analytical framework for real-time analysis
    - [ ]  Consider: OpenAI model-testing eval frameworks and scripts
    - [ ]  Consider: Vector embedding space 3d visualization between ‘gold standard’ and GPT answer
- [ ]  Incorporate ‘bias mitigation’ AI architectures and LLM oversight frameworks

## Ethical Considerations and Compliance

We seek to uphold high standards of ethical research and data privacy. We welcome feedback, suggestions, and partnerships to refine our approach, enhance our platform, and drive the conversation on ethical AI in healthcare forward.

## Enjoy!

Thank you for joining us on this critical journey towards unbiased, ethical AI in clinical decision-making. Together, we can pave the way for a future where technology in healthcare is equitable, safe, and aligned with the highest standards of care. 😊
    """
    )

if __name__ == "__main__":
    run()
