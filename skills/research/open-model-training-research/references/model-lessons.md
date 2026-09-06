# Model training lessons and primary sources

These are source-reported observations, not independently reproduced training runs. Recheck live model licenses and version-specific cards before deployment.

## GLM
- GLM-5 base budget: 28.5T tokens across pretraining/mid-training; 744B total, 40B active. Web/code/math/science curation differs per domain; the math/science exclusion of synthetic material does not mean all training excluded synthetic data.
- GLM-5 SFT retains wrong trajectory segments as context while masking their loss. Transferable procedure: preserve an observed failure and verified correction, not an invented success story.
- GLM-5.3 card says same base as GLM-5.2 and gains from post-training. Do not apply Flash's separate 30T multimodal recipe to this checkpoint.
- GLM-5.3 config: 78 layers, 256 routed experts, 1 shared expert, 8 selected per token, max_position_embeddings 1048576. A config limit is not measured recall quality.
- Model license is GLM-5.3 License, not automatically the code repository's Apache license.
Sources: https://arxiv.org/html/2602.15763v1 ; https://huggingface.co/zai-org/GLM-5.3 ; https://huggingface.co/zai-org/GLM-5.3/raw/main/config.json ; https://huggingface.co/zai-org/GLM-5.3/raw/main/LICENSE

## DeepSeek / Qwen
- DeepSeek-V3: 671B total/37B active, 14.8T pretraining tokens, MLA, MoE, multi-token prediction. Reported GPU-hours do not include every cost of developing a model.
- R1-Zero uses RL without preliminary SFT; R1 adds cold-start data and staged SFT/RL. Outcome verification is not equivalent to rewarding verbose answers.
- Qwen2.5 reports 18T pretraining and over one million SFT examples plus DPO/GRPO. It does not release a complete corpus manifest.
- Qwen2.5-72B-Instruct uses Qwen License Agreement; Qwen2-72B uses Tongyi Qianwen licensing. Check variants separately.
Sources: https://arxiv.org/html/2412.19437v2 ; https://arxiv.org/html/2501.12948v1 ; https://arxiv.org/html/2412.15115v2 ; https://huggingface.co/Qwen/Qwen2.5-72B-Instruct ; https://huggingface.co/Qwen/Qwen2-72B

## Kimi
- Kimi K2 initial model card: 1T rounded total, 32B active, 15.5T tokens, MuonClip. Technical report gives 1.04T total.
- Agentic data includes task rubrics and real/synthetic tools; paper reports 3000+ MCP tools and over 20,000 synthetic tools. Rubric-based critics still risk favoring unwarranted confidence.
- Modified MIT is not identical to unmodified MIT. Initial K2 is not the later thinking checkpoint.
Sources: https://huggingface.co/moonshotai/Kimi-K2-Instruct ; https://arxiv.org/html/2507.20534v1

## Llama / Gemma / SmolLM
- Llama 3.1 flagship: 405B, 15.6T text tokens, SFT/rejection sampling/DPO. Weight release does not reveal the whole training corpus; Community License is custom.
- Gemma 2: 2B/9B/27B trained on 2T/8T/13T tokens; 2B and 9B use knowledge distillation. Include teacher costs and terms when comparing with scratch training.
- SmolLM2 1.7B: about 11T training tokens, staged data mix, SmolTalk SFT and UltraFeedback DPO. GPT-2 tokenizer is an ablation detail; main recipe uses a 49,152-token tokenizer. Public data components include FineMath and Stack-Edu.
Sources: https://arxiv.org/html/2407.21783v3 ; https://huggingface.co/meta-llama/Llama-3.1-8B ; https://arxiv.org/html/2408.00118v3 ; https://ai.google.dev/gemma/terms ; https://arxiv.org/html/2502.02737v1 ; https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B

## OLMo
- OLMo 2 32B processes about 6T tokens from a source mixture around 3.9T: processed and unique tokens differ.
- Dolmino source pool is around 843B tokens; 32B mid-training uses sampled 100B/300B mixes and checkpoint merging, not one pass over every source token.
- Model/code, data mixtures, intermediate checkpoints and logs are published. Model/code Apache terms do not replace source dataset terms.
- Study OLMo for reproducible pipeline details, not as proof of best performance on every task.
Sources: https://allenai.org/blog/olmo2-32b ; https://huggingface.co/allenai/OLMo-2-0325-32B ; https://huggingface.co/datasets/allenai/olmo-mix-1124 ; https://huggingface.co/datasets/allenai/dolmino-mix-1124
