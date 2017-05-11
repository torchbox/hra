import $ from '../globals';

function faqs() {

    var faqMatch = function() {

        var $question               = $( '.faq-questions__item' ),
            $answer                 = $( '.faq-answers__item' ),
            $answerList             = $( '.faq-panel--answers' ),
            $questionList           = $( '.faq-panel--questions' ),
            $answerClose            = $( '.faq-answers__close-answer' ),
            answersDisplay          = 'faq-panel--answers-display',
            questionsHide           = 'faq-panel--questions-hide',
            questionSelected        = 'faq-questions__item--selected',
            answerSelected          = 'faq-answers__item--selected',
            answerDisplay           = 'faq-answers__item--display';

        function deselectQuestions() {
            $question.removeClass( questionSelected );
        }

        function deselectAnswers() {
            $answer.removeClass( answerSelected );
            $answer.removeClass( answerDisplay );
        }

        function selectQuestion( $selectedQuestion ) {
            $selectedQuestion.addClass( questionSelected );
        }

        function showAnswers() {
            setTimeout(function() {
                $answerList.addClass( answersDisplay );
                $questionList.addClass( questionsHide );
            }, 100);
        }

        function hideAnswers() {
            $answerList.removeClass( answersDisplay );
            $questionList.removeClass( questionsHide );
        }

        function selectAnswer( questionData ) {

            var $answer = $answerList.find('[data-faq-answer="' + questionData + '"]');

            $answer.addClass( answerSelected );

            setTimeout(function() {
                $answer.addClass( answerDisplay );
            }, 100);
        }

        function positionAnswer() {

            if ( $(window).width() >= 700 ) {

                var $windowHeight       = $( window ).outerHeight(),
                    $itemHeight         = $answerList.outerHeight(),
                    topValue            = (($windowHeight - $itemHeight) / 2);

                console.log($windowHeight);

                $answerList.css({
                    'top' : topValue
                });
            }
        }

        function bindEvents() {
            $question.on( 'click', function( e ) {
                e.preventDefault();

                var $selectedQuestion       = $(this),
                    questionData            = $(this).attr( 'data-faq-question' );

                // Make all questions 'inactive'
                deselectQuestions();

                // Hide answers
                deselectAnswers();

                // Make selected question 'active'
                selectQuestion( $selectedQuestion );

                // Get correct answer
                selectAnswer( questionData );

                // TODO: only on desktop
                showAnswers();

                // Centre answer
                // positionAnswer();

            });

            // Close answer with icon
            $answerClose.on( 'click', function() {
                hideAnswers();
            });

            // Close answer with swipe
            // if ( $question.length ) {
            //     $answerList.swipe( {
            //         swipe: function(event, direction) {
            //             if ( direction === 'right' ) {
            //                 hideAnswers();
            //             }
            //         }
            //     });
            // }
        }

        // positionAnswer();
        bindEvents();

    };
    
    faqMatch();




    var faqStick = function() {

        if ( $( '.faq-panel--answers' ).length ) {

            var $header             = $( '.site-header' ),
                $faqAnswers         = $( '.faq-panel--answers' ),
                headerTop           = $header.offset().top,
                headerHeight        = $header.outerHeight(),
                faqAnswersFixed     = 'faq-panel--fixed';

            $( window ).scroll(function(){
                if( $( window ).scrollTop() > ( headerTop + headerHeight ) ){
                    $faqAnswers.addClass( faqAnswersFixed );
                } else {
                    $faqAnswers.removeClass( faqAnswersFixed );
                }
            });
        }
    };

    faqStick();
}

export default faqs;