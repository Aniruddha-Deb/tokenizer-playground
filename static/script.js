const inputText = document.getElementById('input-text');
const tokenizedText = document.getElementById('tokenized-text');
const maxTokens = document.getElementById('max-tokens');
const tokenizerSelect = document.getElementById('tokenizer');
const responseFormatRadios = document.querySelectorAll('input[name="response-format"]');

const tokenColors = [
    'pastel-color-1',
    'pastel-color-2',
    'pastel-color-3',
    'pastel-color-4',
    'pastel-color-5',
    'pastel-color-6',
    'pastel-color-7',
    'pastel-color-8',
    'pastel-color-9',
    'pastel-color-10'
];

inputText.addEventListener('input', updateTokenizedText);
responseFormatRadios.forEach(radio => {
    radio.addEventListener('change', handleInputUpdate);
});
tokenizerSelect.addEventListener('change', handleInputUpdate);

let lastSelectedResponseFormat = '';
let lastSelectedTokenizer = '';
function handleInputUpdate() {
    const selectedResponseFormat = document.querySelector('input[name="response-format"]:checked').value;
    const selectedTokenizer = tokenizerSelect.value;

    if (
        selectedResponseFormat !== lastSelectedResponseFormat ||
        selectedTokenizer !== lastSelectedTokenizer
    ) {
        lastSelectedResponseFormat = selectedResponseFormat;
        lastSelectedTokenizer = selectedTokenizer;
        updateTokenizedText();
    }
}

// Generate a random non-repeating sequence of indices for colors
function generateRandomColorSequence(length) {
    const indices = Array.from({ length }, (_, index) => index);
    for (let i = length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [indices[i], indices[j]] = [indices[j], indices[i]];
    }
    return indices;
}

let colorSequence = generateRandomColorSequence(tokenColors.length);

function updateTokenizedText() {
    const selectedTokenizer = tokenizerSelect.value;
    const text = inputText.value;

    fetch('/api/get_tokens', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text, tokenizer: selectedTokenizer }),
    })
    .then(response => response.json())
    .then(data => {
        const response = data;
        const responseFormat = document.querySelector('input[name="response-format"]:checked').value;
        const useNumericIds = (responseFormat === 'numeric-ids');
        const tokenizerType = tokenizerSelect.value;

        var paddingStr = ""
        if (tokenizerType.startsWith('llama')) {
            paddingStr = 'style="padding-left: 4px; padding-right: 4px;"'
        }

        maxTokens.textContent = `Num Tokens: ${response.num_tokens}`;

        let tokenizedHTML = '';
        let tokenCounter = 0;

        if (useNumericIds) {
            response.tokens_int.forEach(token => {
                tokenizedHTML += `${token} `;
                tokenCounter++;
            })
        }
        else {
            console.log(response.tokens_str)
            response.tokens_str.forEach(token => {
                // token = token.replace(/ /g, '&nbsp;')
                // token = token.replace(/\n/g, '<br>')
                const colorIndex = colorSequence[tokenCounter%colorSequence.length];
                const colorClass = `token ${tokenColors[colorIndex]}`;

                tokenizedHTML += `<mark class="${colorClass}" ${paddingStr}>${token}</mark>`;
                tokenCounter++;
            });
        }

        tokenizedText.innerHTML = `<pre>${tokenizedHTML}</pre>`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
