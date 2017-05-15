import $ from '../globals';

function faqs() {

    const $question             = $('.faq-questions__item'),
        $answer                 = $('.faq-answers__item'),
        $answerList             = $('.faq-panel--answers'),
        $questionList           = $('.faq-panel--questions'),
        $answerClose            = $('.faq-answers__close-answer'),
        answersDisplay          = 'faq-panel--answers-display',
        questionsHide           = 'faq-panel--questions-hide',
        questionSelected        = 'faq-questions__item--selected',
        answerSelected          = 'faq-answers__item--selected',
        answerDisplay           = 'faq-answers__item--display',
        timeout                 = 100,
        mobileBreakpoint        = 800;

    function deselectQuestions() {
        $question.removeClass(questionSelected);
    }

    function deselectAnswers() {
        $answer.removeClass(answerSelected);
        $answer.removeClass(answerDisplay);
    }

    function selectQuestion($selectedQuestion) {
        $selectedQuestion.addClass(questionSelected);
    }

    function showAnswers() {
        setTimeout(function() {
            $answerList.addClass(answersDisplay);
            $questionList.addClass(questionsHide);
        }, timeout);
    }

    function hideAnswers() {
        $answerList.removeClass(answersDisplay);
        $questionList.removeClass(questionsHide);
    }

    function selectAnswer(questionData) {
        const $answer = $answerList.find('[data-faq-answer="' + questionData + '"]');

        $answer.addClass(answerSelected);

        setTimeout(function() {
            $answer.addClass(answerDisplay);
        }, timeout);
    }

    function positionAnswer() {
        if ($(window).width() >= mobileBreakpoint) {
            const $windowHeight     = $(window).outerHeight(),
                $itemHeight         = $answerList.outerHeight(),
                topValue            = (($windowHeight - $itemHeight) / 2);

            $answerList.css({
                'top' : topValue + 50
            });

            showAnswers();
        }
    }

    function bindEvents() {
        $question.on('click', function(e) {
            e.preventDefault();

            const $selectedQuestion      = $(this),
                questionData             = $(this).attr('data-faq-question');

            // Make all questions 'inactive'
            deselectQuestions();

            // Hide answers
            deselectAnswers();

            // Make selected question 'active'
            selectQuestion($selectedQuestion);

            // Get correct answer
            selectAnswer(questionData);

            // Centre answer
            positionAnswer();

        });

        // Close answer with icon
        $answerClose.on('click', () => hideAnswers());
    }

    if ($('.faq-questions__item').length) {
        positionAnswer();
        bindEvents();
    }

}
    
export default faqs;