const surveyContainer = document.getElementById('surveyContainer');
const refContainer = document.getElementById('refContainer');
const prevButton = document.getElementById('prevButton');
const nextButton = document.getElementById('nextButton');
const submitButton = document.getElementById('submitButton');
const refImg = document.getElementById('refImg');
const tarImg = document.getElementById('tarImg');
// const criteria = document.getElementById('item');
const pageNum = document.getElementById('page-number');

var questions = new Array();
var uid;
var totalNum;

const answers = {};

let currentQuestionIndex = 0;

function loadImage(img_path){
    var imgUrl = `/images/${img_path}`;
    return imgUrl;
}


async function loadQuestions() {
    const response = await fetch('/api/questions');
    const body = await response.json();
    questions = body.data
    uid = body.uid
    console.log(questions)
    totalNum = questions.length;
    
}


function createQuestion(index) {
    surveyContainer.innerHTML = '';
    // refContainer.innerHTML = '';
    const questionObj = questions[index];

    pageNum.innerHTML = `${index+1} / ${totalNum}`;

    const refImgUrl = loadImage(questionObj.ref_img);
    refImg.src = `${refImgUrl}?v=1.0`;
    const tarImgUrl = loadImage(questionObj.tar_img);
    tarImg.src = `${tarImgUrl}?v=1.0`;

    for (const option of questionObj.options) {
        const optionContainer = document.createElement('div');
        optionContainer.classList.add('option-container');

        const input = document.createElement('input');
        input.type = 'radio';
        input.id = option;
        input.name = index.toString();
        // input.value = "";

        const img = document.createElement('img');
        const imgUrl = loadImage(option);
        img.src = `${imgUrl}?v=1.0`;
        img.classList.add('option-image');

        img.addEventListener('click', () => {
            // const curChecked = document.querySelector(`input[name="${index}"]:checked`);
            // console.log(curChecked)

            // if (curChecked) {
            //     input.checked = false;
            // }
            input.checked = true;
            answers[index] = option;
            console.log(answers)
        });

        optionContainer.appendChild(img);
        optionContainer.appendChild(input);
        optionContainer.classList.add('hc-container');
        surveyContainer.appendChild(optionContainer);

        if (answers[index] === option) {
            input.checked = true;
        }
    }

    prevButton.disabled = index === 0;
    nextButton.disabled = index === questions.length - 1;

    if (prevButton.disabled){ prevButton.style.color='#9C9C9C';}
    else { prevButton.style.color='#1C1C1C';}
    if (nextButton.disabled){ nextButton.style.color='#9C9C9C';}
    else { nextButton.style.color='#1C1C1C';}

    let cnt = Object.keys(answers).length;
    if (cnt === questions.length){
        submitButton.classList.add('button2');
        submitButton.classList.remove('button');
    } else {submitButton.classList.add('button');
            submitButton.classList.remove('button2');
    }
}

prevButton.addEventListener('click', () => {
    const selectedOption = document.querySelector(`input[name="${currentQuestionIndex}"]:checked`);

    if (selectedOption) {
        answers[currentQuestionIndex] = selectedOption.id;
    }

    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        createQuestion(currentQuestionIndex);
    }
});

nextButton.addEventListener('click', () => {
    const selectedOption = document.querySelector(`input[name="${currentQuestionIndex}"]:checked`);
    if (selectedOption) {
        answers[currentQuestionIndex] = selectedOption.id;
    }

    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        createQuestion(currentQuestionIndex);
    }
});

submitButton.addEventListener('click', () => {
    const selectedOption = document.querySelector(`input[name="${currentQuestionIndex}"]:checked`);
    if (selectedOption) {
        answers[currentQuestionIndex] = selectedOption.id;
    }

    event.preventDefault();
    
    let cnt = Object.keys(answers).length;
    if (cnt != questions.length){
        alert(`请回答完所有问题后再点击提交\n目前还有 ${questions.length-cnt} 道题目未回答`);
    }
    else {
        const formData = {
            'uid': uid,
            "answer": answers
        };


        fetch('/submit', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            alert(data.message);
            currentQuestionIndex = 0;
            Object.keys(answers).forEach(key => delete answers[key]);
            window.location.href = '/thanks';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('提交失败，请重试');
        });
    }

});

loadQuestions().then(() => {
    createQuestion(currentQuestionIndex);
});
