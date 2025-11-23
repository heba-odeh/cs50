import sys
import tensorflow as tf
from transformers import AutoTokenizer, TFBertForMaskedLM
from PIL import Image, ImageDraw, ImageFont

MODEL = "bert-base-uncased"
K = 3  # number of predictions

# Constants for visualization
FONT = ImageFont.load_default()  # or specify your own font file if available
GRID_SIZE = 40
PIXELS_PER_WORD = 200

def main():
    text = input("Text: ")

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = TFBertForMaskedLM.from_pretrained(MODEL)

    inputs = tokenizer(text, return_tensors="tf")
    input_ids = inputs["input_ids"]

    mask_token_index = tf.where(input_ids == tokenizer.mask_token_id)
    if len(mask_token_index) == 0:
        sys.exit(f"Input must include the mask token {tokenizer.mask_token}.")

    mask_index = mask_token_index[0][1].numpy()

    outputs = model(**inputs, output_attentions=True)
    logits = outputs.logits
    attentions = outputs.attentions  # tuple: (num_layers, batch, heads, seq_len, seq_len)

    mask_token_logits = logits[0, mask_index]
    top_k = tf.math.top_k(mask_token_logits, k=K)

    for token_id in top_k.indices.numpy():
        predicted_token = tokenizer.decode([token_id]).strip()
        print(text.replace(tokenizer.mask_token, predicted_token))

    tokens = tokenizer.convert_ids_to_tokens(input_ids[0].numpy())
    visualize_attentions(tokens, attentions)

def get_color_for_attention_score(score):
    # score expected in [0, 1], map to grayscale 255 = white (high attention), 0 = black
    gray = int(255 * score)
    return (gray, gray, gray)

def visualize_attentions(tokens, attentions):
    # attentions is a tuple of length num_layers
    for layer_idx, layer_attention in enumerate(attentions):
        # layer_attention shape: (batch_size=1, num_heads, seq_len, seq_len)
        layer_attention = layer_attention[0]  # remove batch dim

        for head_idx in range(layer_attention.shape[0]):
            attention_weights = layer_attention[head_idx].numpy()  # (seq_len, seq_len)
            generate_diagram(layer_idx + 1, head_idx + 1, tokens, attention_weights)

def generate_diagram(layer_number, head_number, tokens, attention_weights):
    size = GRID_SIZE * len(tokens) + PIXELS_PER_WORD
    img = Image.new("RGBA", (size, size), "black")
    draw = ImageDraw.Draw(img)

    # Draw tokens on top (columns)
    for i, token in enumerate(tokens):
        token_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        token_draw = ImageDraw.Draw(token_img)
        token_draw.text((size - PIXELS_PER_WORD + 5, PIXELS_PER_WORD + i * GRID_SIZE), token, fill="white", font=FONT)
        token_img = token_img.rotate(90, expand=1)
        img.paste(token_img, mask=token_img)

    # Draw tokens on left (rows)
    for i, token in enumerate(tokens):
        _, _, w, _ = draw.textbbox((0, 0), token, font=FONT)
        draw.text((PIXELS_PER_WORD - w - 5, PIXELS_PER_WORD + i * GRID_SIZE), token, fill="white", font=FONT)

    # Draw attention heatmap
    for i in range(len(tokens)):
        for j in range(len(tokens)):
            x = PIXELS_PER_WORD + j * GRID_SIZE
            y = PIXELS_PER_WORD + i * GRID_SIZE
            color = get_color_for_attention_score(attention_weights[i][j])
            draw.rectangle([x, y, x + GRID_SIZE, y + GRID_SIZE], fill=color)

    filename = f"Attention_Layer{layer_number}_Head{head_number}.png"
    img.save(filename)
    print(f"Saved attention visualization: {filename}")

if __name__ == "__main__":
    main()

