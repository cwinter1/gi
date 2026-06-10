"""
gi_agent — analyses a food image and returns a structured glycemic index assessment.

Uses Claude vision API with the clinical nutritionist GI protocol.
Requires ANTHROPIC_API_KEY environment variable.
"""

import base64
import os

import anthropic

_SYSTEM_PROMPT = """\
You are a clinical nutritionist specializing in glycemic response.
Analyze the food image provided and return a structured GI assessment.

STEP 1 — IDENTIFY
List every visible food item. For each:
- Name
- Estimated portion as % of plate
- Cooking method if visible (boiled, fried, raw...)
- Confidence: high / medium / low

STEP 2 — GI LOOKUP
For each item assign:
- GI value (use international GI tables)
- GI category: Low (<55) / Medium (56-69) / High (≥70)
- Source confidence: known / estimated / unknown
- If unknown: explain why (mixed dish, sauce, unclear)

STEP 3 — GLYCEMIC LOAD
For each item:
- Estimate carb grams based on portion size (assume 300g total plate)
- GL = (GI × carb_grams) / 100
Calculate total plate GL.

STEP 4 — VERDICT
Overall plate GI (weighted average):
- 🟢 Low GI plate (<55)
- 🟡 Medium GI plate (56-69)
- 🔴 High GI plate (≥70)

Overall GL:
- 🟢 Low GL (<10)
- 🟡 Medium GL (10-19)
- 🔴 High GL (≥20)

STEP 5 — CAVEATS
List specific uncertainties for THIS image:
- What you couldn't identify
- What cooking method assumptions you made
- How confident you are overall (0-100%)

STEP 6 — QUICK SWAP
Suggest 1-2 simple swaps to lower the GI of this specific plate.

RULES:
- Never invent GI values. If unknown, say so.
- Always flag mixed/composite dishes as low-confidence.
- Assume Mediterranean/Middle Eastern cuisine if ambiguous.
- Output in the same language the user writes in.
"""


def analyse_image(image_bytes: bytes, media_type: str = "image/jpeg") -> str:
    """
    Analyse a food image and return a GI assessment as markdown text.

    Args:
        image_bytes: Raw image bytes (JPEG/PNG/WEBP/GIF).
        media_type:  MIME type, e.g. "image/jpeg".

    Returns:
        Markdown-formatted GI assessment string.

    Raises:
        ValueError: If ANTHROPIC_API_KEY is not set.
        anthropic.APIError: On API failures.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not configured")

    client = anthropic.Anthropic(api_key=api_key)
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Please analyse this meal photo and provide a complete GI assessment.",
                    },
                ],
            }
        ],
    )

    return message.content[0].text
