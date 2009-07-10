/*
Scripts for cnprog.com
Project Name: Lanai
All Rights Resevred 2008. CNPROG.COM
*/
var lanai =
{
    /**
     * Finds any <pre><code></code></pre> tags which aren't registered for
     * pretty printing, adds the appropriate class name and invokes prettify.
     */
    highlightSyntax: function(){
        var styled = false;
        $("pre code").parent().each(function(){
            if (!$(this).hasClass('prettyprint')){
                $(this).addClass('prettyprint');
                styled = true;
            }
        });

        if (styled){
            prettyPrint();
        }
    }
};

var Vote = function(){
    // All actions are related to a question
    var questionId;
    // The object we operate on actually. It can be a question or an answer.
    var postId;
    var questionAuthorId;
    var currentUserId;
    var answerContainerIdPrefix = 'answer-container-';
    var voteContainerId = 'vote-buttons';
    var imgIdPrefixAccept = 'answer-img-accept-';
    var imgClassPrefixFavorite = 'question-img-favorite';
    var imgIdPrefixQuestionVoteup = 'question-img-upvote-';
    var imgIdPrefixQuestionVotedown = 'question-img-downvote-';
    var imgIdPrefixAnswerVoteup = 'answer-img-upvote-';
    var imgIdPrefixAnswerVotedown = 'answer-img-downvote-';
    var divIdFavorite = 'favorite-number';
    var commentLinkIdPrefix = 'comment-';
    var voteNumberClass = "vote-number";
    var offensiveIdPrefixQuestionFlag = 'question-offensive-flag-';
    var offensiveIdPrefixAnswerFlag = 'answer-offensive-flag-';
    var offensiveClassFlag = 'offensive-flag';
    var questionControlsId = 'question-controls';
    var removeQuestionLinkIdPrefix = 'question-delete-link-';
    var removeAnswerLinkIdPrefix = 'answer-delete-link-';
    
    var acceptAnonymousMessage = $.i18n._('insufficient privilege');
    var acceptOwnAnswerMessage = $.i18n._('cannot pick own answer as best');
    var favoriteAnonymousMessage = $.i18n._('anonymous user cannot select favorite questions') 
					+ "<a href='/account/signin/?next=/questions/{{QuestionID}}'>"
					+ $.i18n._('please login') + "</a>";
    var voteAnonymousMessage = $.i18n._('anonymous users cannot vote') 
					+ "<a href='/account/signin/?next=/questions/{{QuestionID}}'>"
					+ $.i18n._('please login') + "</a>";
    var upVoteRequiredScoreMessage = $.i18n._('>15 points requried to upvote') 
					+ $.i18n._('please see') + "<a href='/faq'>faq</a>";
    var downVoteRequiredScoreMessage = $.i18n._('>100 points requried to downvote')
					+ $.i18n._('please see') + "<a href='/faq'>faq</a>";
    var voteOwnDeniedMessage = $.i18n._('cannot vote for own posts');
    var voteRequiredMoreVotes = $.i18n._('daily vote cap exhausted')
					+ $.i18n._('please see') + "<a href='/faq'>faq</a>";
    var voteDenyCancelMessage = $.i18n._('cannot revoke old vote')
					+ $.i18n._('please see') + "<a href='/faq'>faq</a>";
    var offensiveConfirmation = $.i18n._('please confirm offensive');
    var offensiveAnonymousMessage = $.i18n._('anonymous users cannot flag offensive posts')
					+ "<a href='/account/signin/?next=/questions/{{QuestionID}}'>"
					+ $.i18n._('please login') + "</a>";
    var offensiveTwiceMessage = $.i18n._('cannot flag message as offensive twice')
					+ $.i18n._('please see') + "<a href='/faq'>faq</a>";
    var offensiveNoFlagsLeftMessage = $.i18n._('flag offensive cap exhausted')
					+ $.i18n._('please see') + "<a href='/faq'>faq</a>";
    var offensiveNoPermissionMessage = $.i18n._('need >15 points to report spam')
					+ $.i18n._('please see') + "<a href='/faq'>faq</a>";
    var removeConfirmation = $.i18n._('confirm delete');
    var removeAnonymousMessage = $.i18n._('anonymous users cannot delete/undelete');
    var recoveredMessage = $.i18n._('post recovered');
    var deletedMessage = $.i18n._('post deleted');
    
    var VoteType = {
        acceptAnswer : 0,
        questionUpVote : 1,
        questionDownVote : 2,
        favorite : 4,
        answerUpVote: 5,
        answerDownVote:6,
        offensiveQuestion : 7,
        offensiveAnswer:8,
        removeQuestion: 9,
        removeAnswer:10
    };

    var getFavoriteButton = function(){
        var favoriteButton = 'div.'+ voteContainerId +' img[class='+ imgClassPrefixFavorite +']';
        return $(favoriteButton);
    };
    var getFavoriteNumber = function(){
        var favoriteNumber = '#'+ divIdFavorite ;
        return $(favoriteNumber);
    };
    var getQuestionVoteUpButton = function(){
        var questionVoteUpButton = 'div.'+ voteContainerId +' img[id^='+ imgIdPrefixQuestionVoteup +']';
        return $(questionVoteUpButton);
    };
    var getQuestionVoteDownButton = function(){
        var questionVoteDownButton = 'div.'+ voteContainerId +' img[id^='+ imgIdPrefixQuestionVotedown +']';
        return $(questionVoteDownButton);
    };
    var getAnswerVoteUpButtons = function(){
        var answerVoteUpButton = 'div.'+ voteContainerId +' img[id^='+ imgIdPrefixAnswerVoteup +']';
        return $(answerVoteUpButton);
    };
    var getAnswerVoteDownButtons = function(){
        var answerVoteDownButton = 'div.'+ voteContainerId +' img[id^='+ imgIdPrefixAnswerVotedown +']';
        return $(answerVoteDownButton);
    };
    var getAnswerVoteUpButton = function(id){
        var answerVoteUpButton = 'div.'+ voteContainerId +' img[id='+ imgIdPrefixAnswerVoteup + id + ']';
        return $(answerVoteUpButton);
    };
    var getAnswerVoteDownButton = function(id){
        var answerVoteDownButton = 'div.'+ voteContainerId +' img[id='+ imgIdPrefixAnswerVotedown + id + ']';
        return $(answerVoteDownButton);
    };
    
    var getOffensiveQuestionFlag = function(){
        var offensiveQuestionFlag = 'table[id=question-table] span[class='+ offensiveClassFlag +']';
        return $(offensiveQuestionFlag);
    };
    
    var getOffensiveAnswerFlags = function(){
        var offensiveQuestionFlag = 'div.answer span[class='+ offensiveClassFlag +']';
        return $(offensiveQuestionFlag);
    };
    
    var getremoveQuestionLink = function(){
        var removeQuestionLink = 'div#question-controls a[id^='+ removeQuestionLinkIdPrefix +']';
        return $(removeQuestionLink);
    };
    
    var getremoveAnswersLinks = function(){
        var removeAnswerLinks = 'div.answer-controls a[id^='+ removeAnswerLinkIdPrefix +']';
        return $(removeAnswerLinks);
    };
   
    var setVoteImage = function(voteType, undo, object){
        var flag = undo ? "" : "-on";
        var arrow = (voteType == VoteType.questionUpVote || voteType == VoteType.answerUpVote) ? "up" : "down";
        object.attr("src", "/content/images/vote-arrow-"+ arrow + flag +".png");
        
        // if undo voting, then undo the pair of arrows.
        if(undo){
            if(voteType == VoteType.questionUpVote || voteType == VoteType.questionDownVote){
                $(getQuestionVoteUpButton()).attr("src", "/content/images/vote-arrow-up.png");
                $(getQuestionVoteDownButton()).attr("src", "/content/images/vote-arrow-down.png");
            }
            else{
                $(getAnswerVoteUpButton(postId)).attr("src", "/content/images/vote-arrow-up.png");
                $(getAnswerVoteDownButton(postId)).attr("src", "/content/images/vote-arrow-down.png");
            }
        }
    };
    
    var setVoteNumber = function(object, number){
        var voteNumber = object.parent('div.'+ voteContainerId).find('div.'+ voteNumberClass);
        $(voteNumber).text(number);
    };
    
    var bindEvents = function(){
        // accept answers
        if(questionAuthorId == currentUserId){
            var acceptedButtons = 'div.'+ voteContainerId +' img[id^='+ imgIdPrefixAccept +']';
            $(acceptedButtons).unbind('click').click(function(event){
               Vote.accept($(event.target))
            });
        }
        // set favorite question
        var favoriteButton = getFavoriteButton();
        favoriteButton.unbind('click').click(function(event){
           Vote.favorite($(event.target))
        });
    
        // question vote up
        var questionVoteUpButton = getQuestionVoteUpButton();
        questionVoteUpButton.unbind('click').click(function(event){
           Vote.vote($(event.target), VoteType.questionUpVote)
        });
    
        var questionVoteDownButton = getQuestionVoteDownButton();
        questionVoteDownButton.unbind('click').click(function(event){
           Vote.vote($(event.target), VoteType.questionDownVote)
        });
    
        var answerVoteUpButton = getAnswerVoteUpButtons();
        answerVoteUpButton.unbind('click').click(function(event){
           Vote.vote($(event.target), VoteType.answerUpVote)
        });
        
        var answerVoteDownButton = getAnswerVoteDownButtons();
        answerVoteDownButton.unbind('click').click(function(event){
           Vote.vote($(event.target), VoteType.answerDownVote)
        });
    
        getOffensiveQuestionFlag().unbind('click').click(function(event){
           Vote.offensive(this, VoteType.offensiveQuestion)
        });
    
        getOffensiveAnswerFlags().unbind('click').click(function(event){
           Vote.offensive(this, VoteType.offensiveAnswer)
        });
    
        getremoveQuestionLink().unbind('click').click(function(event){
            Vote.remove(this, VoteType.removeQuestion);
        });
    
        getremoveAnswersLinks().unbind('click').click(function(event){
            Vote.remove(this, VoteType.removeAnswer)
        });
    };
    
    var submit = function(object, voteType, callback) {
        $.ajax({
            type: "POST",
            cache: false,
            dataType: "json",
            url: "/questions/" + questionId + "/vote/",
            data: { "type": voteType, "postId": postId },
            error: handleFail,
            success: function(data){callback(object, voteType, data)}});
    };
    
    var handleFail = function(xhr, msg){
        alert("Callback invoke error: " + msg)
    };

    // callback function for Accept Answer action
    var callback_accept = function(object, voteType, data){
        if(data.allowed == "0" && data.success == "0"){
            showMessage(object, acceptAnonymousMessage);
        }
        else if(data.allowed == "-1"){
            showMessage(object, acceptOwnAnswerMessage);
        }
        else if(data.status == "1"){
            object.attr("src", "/content/images/vote-accepted.png");
            $("#"+answerContainerIdPrefix+postId).removeClass("accepted-answer");
            $("#"+commentLinkIdPrefix+postId).removeClass("comment-link-accepted");
        }
        else if(data.success == "1"){
            var acceptedButtons = 'div.'+ voteContainerId +' img[id^='+ imgIdPrefixAccept +']';
            $(acceptedButtons).attr("src", "/content/images/vote-accepted.png");
            var answers = ("div[id^="+answerContainerIdPrefix +"]");
            $(answers).removeClass("accepted-answer");
            var commentLinks = ("div[id^="+answerContainerIdPrefix +"] div[id^="+ commentLinkIdPrefix +"]");
            $(commentLinks).removeClass("comment-link-accepted");
            
            object.attr("src", "/content/images/vote-accepted-on.png");
            $("#"+answerContainerIdPrefix+postId).addClass("accepted-answer");
            $("#"+commentLinkIdPrefix+postId).addClass("comment-link-accepted");
        }
        else{
            showMessage(object, data.message);
        }
    };

    var callback_favorite = function(object, voteType, data){
        if(data.allowed == "0" && data.success == "0"){
            showMessage(object, favoriteAnonymousMessage.replace("{{QuestionID}}", questionId));
        }
        else if(data.status == "1"){
            object.attr("src", "/content/images/vote-favorite-off.png");
            var fav = getFavoriteNumber();
            fav.removeClass("my-favorite-number");
            if(data.count == 0)
                data.count = '';
            fav.text(data.count);
        }
        else if(data.success == "1"){
            object.attr("src", "/content/images/vote-favorite-on.png");
            var fav = getFavoriteNumber();
            fav.text(data.count);
            fav.addClass("my-favorite-number");
        }
        else{
            showMessage(object, data.message);
        }
    };
        
    var callback_vote = function(object, voteType, data){
        if(data.allowed == "0" && data.success == "0"){
            showMessage(object, voteAnonymousMessage.replace("{{QuestionID}}", questionId));
        }
        else if(data.allowed == "-3"){
            showMessage(object, voteRequiredMoreVotes);
        }
        else if(data.allowed == "-2"){
            if(voteType == VoteType.questionUpVote || voteType == VoteType.answerUpVote){
                showMessage(object, upVoteRequiredScoreMessage);
            }
            else if(voteType == VoteType.questionDownVote || voteType == VoteType.answerDownVote){
                showMessage(object, downVoteRequiredScoreMessage);
            }
        }
        else if(data.allowed == "-1"){
            showMessage(object, voteOwnDeniedMessage);
        }
        else if(data.status == "2"){
            showMessage(object, voteDenyCancelMessage);
        }
        else if(data.status == "1"){
            setVoteImage(voteType, true, object);
            setVoteNumber(object, data.count);
        }     
        else if(data.success == "1"){
            setVoteImage(voteType, false, object);
            setVoteNumber(object, data.count);
            if(data.message.length > 0)
                showMessage(object, data.message);
        }
    };
        
    var callback_offensive = function(object, voteType, data){
        object = $(object);
        if(data.allowed == "0" && data.success == "0"){
            showMessage(object, offensiveAnonymousMessage.replace("{{QuestionID}}", questionId));
        }
        else if(data.allowed == "-3"){
            showMessage(object, offensiveNoFlagsLeftMessage);
        }  
        else if(data.allowed == "-2"){
            showMessage(object, offensiveNoPermissionMessage);
        }  
        else if(data.status == "1"){
            showMessage(object, offensiveTwiceMessage);
        }  
        else if(data.success == "1"){
            $(object).children('span[class=darkred]').text("("+ data.count +")");
        }
    };
        
    var callback_remove = function(object, voteType, data){
		alert(data.status);
        if(data.allowed == "0" && data.success == "0"){
            showMessage(object, removeAnonymousMessage.replace("{{QuestionID}}", questionId));
        }
        else if (data.success == "1"){
			if (removeActionType == 'delete'){
				postNode.addClass('deleted');
				postRemoveLink.innerHTML = $.i18n._('undelete');
        		showMessage(object, deletedMessage);
			}
			else if (removeActionType == 'undelete') {
				postNode.removeClass('deleted');
				postRemoveLink.innerHTML = $.i18n._('delete');
            	showMessage(object, recoveredMessage);
			}
		}
    };
        
    return {
        init : function(qId, questionAuthor, userId){
            questionId = qId;
            questionAuthorId = questionAuthor;
            currentUserId = userId;
            bindEvents();
        },
        
        // Accept answer public function
        accept: function(object){
            postId = object.attr("id").substring(imgIdPrefixAccept.length);
            submit(object, VoteType.acceptAnswer, callback_accept);
        },
        
        favorite: function(object){
            if(!currentUserId || currentUserId.toUpperCase() == "NONE"){
                showMessage(object, favoriteAnonymousMessage.replace("{{QuestionID}}", questionId));
                return false;
            }
            submit(object, VoteType.favorite, callback_favorite);
        },
            
        vote: function(object, voteType){
            if(!currentUserId || currentUserId.toUpperCase() == "NONE"){
                showMessage(object, voteAnonymousMessage.replace("{{QuestionID}}", questionId));
                return false;   
            }
            if(voteType == VoteType.answerUpVote){
                postId = object.attr("id").substring(imgIdPrefixAnswerVoteup.length);
            }
            else if(voteType == VoteType.answerDownVote){
                postId = object.attr("id").substring(imgIdPrefixAnswerVotedown.length);
            }
            
            submit(object, voteType, callback_vote);
        },
        
        offensive: function(object, voteType){
            if(!currentUserId || currentUserId.toUpperCase() == "NONE"){
                showMessage($(object), offensiveAnonymousMessage.replace("{{QuestionID}}", questionId));
                return false;   
            }
            if(confirm(offensiveConfirmation)){
                postId = object.id.substr(object.id.lastIndexOf('-') + 1);
                submit(object, voteType, callback_offensive);
            }
        },
            
        remove: function(object, voteType){
            if(!currentUserId || currentUserId.toUpperCase() == "NONE"){
                showMessage($(object), removeAnonymousMessage.replace("{{QuestionID}}", questionId));
                return false;   
            }
            if(confirm(removeConfirmation)){
				bits = object.id.split('-');
				postId = bits.pop();/* this seems to be used within submit! */
				postType = bits.shift();

				if (postType == 'answer'){
					postNode = $('#answer-container-' + postId);
					postRemoveLink = object;
					if (postNode.hasClass('deleted')){
						removeActionType = 'undelete';
					}
					else {
						removeActionType = 'delete';
					}
				}
                submit($(object), voteType, callback_remove);


            }
        }
    }
} ();


// site comments
function createComments(type) {
    var objectType = type;
    var jDivInit = function(id) {
        return $("#comments-" + objectType + '-' + id);
    };

    var appendLoaderImg = function(id) {
        appendLoader("#comments-" + objectType + '-' + id + " div.comments");
    };

    var canPostComments = function(id, jDiv) {
        var jHidden = jDiv.siblings("#can-post-comments-" + objectType + '-' + id);
        return jHidden.val().toLowerCase() == "true";
    };

    var renderForm = function(id, jDiv) {
        var formId = "form-comments-" + objectType + "-" + id;
        if (canPostComments(id, jDiv)) {
            if (jDiv.find("#" + formId).length == 0) {
                var form = '<form id="' + formId + '" class="post-comments"><div>';
                form += '<textarea name="comment" cols="60" rows="5" maxlength="300" onblur="'+ objectType +'Comments.updateTextCounter(this)" ';
                form += 'onfocus="' + objectType + 'Comments.updateTextCounter(this)" onkeyup="'+ objectType +'Comments.updateTextCounter(this)"></textarea>';
                form += '<input type="submit" value="'
						+ $.i18n._('add comment') + '" /><br><span class="text-counter"></span>';
                form += '<span class="form-error"></span></div></form>';

                jDiv.append(form);

                setupFormValidation("#" + formId,
                    { comment: { required: true, minlength: 10} }, '',
                    function() { postComment(id, formId); });
            }
        }
        else {
            var divId = "comments-rep-needed-" + objectType + '-' + id;
            if (jDiv.find("#" + divId).length == 0) {
                jDiv.append('<div id="' + divId + '" style="color:red">'
					+ $.i18n._('to comment, need') + ' ' +
					+ repNeededForComments + ' ' + $.i18n._('community reputation points')
					+ '<a href="/faq" class="comment-user">' + $.i18n._('please see') + 'faq</a></span>');
            }
        }
    };

    var getComments = function(id, jDiv) {
        appendLoaderImg(id);
        $.getJSON("/" + objectType + "s/" + id + "/comments/", function(json) { showComments(id, json); });
    };

    var showComments = function(id, json) {
        var jDiv = jDivInit(id);

        jDiv = jDiv.find("div.comments");   // this div should contain any fetched comments..
        jDiv.find("div[id^='comment-" + objectType + "-'" + "]").remove();  // clean previous calls..

        removeLoader();

        if (json && json.length > 0) {
            for (var i = 0; i < json.length; i++)
                renderComment(jDiv, json[i]);

            jDiv.children().show();
        }
    };

    // {"Id":6,"PostId":38589,"CreationDate":"an hour ago","Text":"hello there!","UserDisplayName":"Jarrod Dixon","UserUrl":"/users/3/jarrod-dixon","DeleteUrl":null}
    var renderComment = function(jDiv, json) {
        var html = '<div id="comment-' + objectType + "-" + json.id + '" style="display:none">' + json.text;
        html += json.user_url ? '&nbsp;&ndash;&nbsp;<a href="' + json.user_url + '"' : '<span';
        html += ' class="comment-user">' + json.user_display_name + (json.user_url ? '</a>' : '</span>');
        html += ' <span class="comment-date">(' + json.add_date + ')</span>';

        if (json.delete_url) {
            var img = "/content/images/close-small.png";
            var imgHover = "/content/images/close-small-hover.png";
            html += '<img onclick="' + objectType + 'Comments.deleteComment($(this), ' + json.object_id + ', \'' + json.delete_url + '\')" src="' + img;
            html += '" onmouseover="$(this).attr(\'src\', \'' + imgHover + '\')" onmouseout="$(this).attr(\'src\', \'' + img
            html += '\')" title="' + $.i18n._('delete this comment') + '" />';
        }

        html += '</div>';

        jDiv.append(html);
    };

    var postComment = function(id, formId) {
        appendLoaderImg(id);

        var formSelector = "#" + formId;
        var textarea = $(formSelector + " textarea");

        $.ajax({
            type: "POST",
            url: "/" + objectType + "s/" + id + "/comments/",
            dataType: "json",
            data: { comment: textarea.val() },
            success: function(json) {
                showComments(id, json);
                textarea.val("");
                commentsFactory[objectType].updateTextCounter(textarea);
                enableSubmitButton(formSelector);
            },
            error: function(res, textStatus, errorThrown) {
                removeLoader();
                showMessage(formSelector, res.responseText);
                enableSubmitButton(formSelector);
            }
        });
    };

    // public methods..
    return {

        init: function() {
            // Setup "show comments" clicks..
            $("a[id^='comments-link-" + objectType + "-" + "']").unbind("click").click(function() { commentsFactory[objectType].show($(this).attr("id").substr(("comments-link-" + objectType + "-").length)); });
        },

        show: function(id) {
            var jDiv = jDivInit(id);
            getComments(id, jDiv);
            renderForm(id, jDiv);
            jDiv.show();
            if (canPostComments(id, jDiv)) jDiv.find("textarea").get(0).focus();
            jDiv.siblings("a").unbind("click").click(function(){ 
													commentsFactory[objectType].hide(id); 
													}).text($.i18n._('hide comments'));
        },

        hide: function(id) {
            var jDiv = jDivInit(id);
            var len = jDiv.children("div.comments").children().length;
            var anchorText = len == 0 ? $.i18n._('add a comment') : $.i18n._('comments') + ' (<b>' + len + "</b>)";

            jDiv.hide();
            jDiv.siblings("a").unbind("click").click(function() { commentsFactory[objectType].show(id); }).html(anchorText);
            jDiv.children("div.comments").children().hide();
        },

        deleteComment: function(jImg, id, deleteUrl) {
            if (confirm($.i18n._('confirm delete comment'))) {
                jImg.hide();
                appendLoaderImg(id);
                $.post(deleteUrl, { dataNeeded: "forIIS7" }, function(json) {
                    showComments(id, json);
                }, "json");
            }
        },

        updateTextCounter: function(textarea) {
            var length = textarea.value ? textarea.value.length : 0;
            var color = length > 270 ? "#f00" : length > 200 ? "#f60" : "#999";
            var jSpan = $(textarea).siblings("span.text-counter");
            jSpan.html($.i18n._('can write')
					+ (300 - length) + ' ' 
					+ $.i18n._('characters')).css("color", color);
        }
    };
}

var questionComments = createComments('question');
var answerComments = createComments('answer');

$().ready(function() {
    questionComments.init();
    answerComments.init();
});

var commentsFactory = {'question' : questionComments, 'answer' : answerComments};

/*
Prettify
http://www.apache.org/licenses/LICENSE-2.0
*/
var PR_SHOULD_USE_CONTINUATION = true; var PR_TAB_WIDTH = 8; var PR_normalizedHtml; var PR; var prettyPrintOne; var prettyPrint; function _pr_isIE6() { var isIE6 = navigator && navigator.userAgent && /\bMSIE 6\./.test(navigator.userAgent); _pr_isIE6 = function() { return isIE6; }; return isIE6; } (function() { function wordSet(words) { words = words.split(/ /g); var set = {}; for (var i = words.length; --i >= 0; ) { var w = words[i]; if (w) { set[w] = null; } } return set; } var FLOW_CONTROL_KEYWORDS = "break continue do else for if return while "; var C_KEYWORDS = FLOW_CONTROL_KEYWORDS + "auto case char const default " + "double enum extern float goto int long register short signed sizeof " + "static struct switch typedef union unsigned void volatile "; var COMMON_KEYWORDS = C_KEYWORDS + "catch class delete false import " + "new operator private protected public this throw true try "; var CPP_KEYWORDS = COMMON_KEYWORDS + "alignof align_union asm axiom bool " + "concept concept_map const_cast constexpr decltype " + "dynamic_cast explicit export friend inline late_check " + "mutable namespace nullptr reinterpret_cast static_assert static_cast " + "template typeid typename typeof using virtual wchar_t where "; var JAVA_KEYWORDS = COMMON_KEYWORDS + "boolean byte extends final finally implements import instanceof null " + "native package strictfp super synchronized throws transient "; var CSHARP_KEYWORDS = JAVA_KEYWORDS + "as base by checked decimal delegate descending event " + "fixed foreach from group implicit in interface internal into is lock " + "object out override orderby params readonly ref sbyte sealed " + "stackalloc string select uint ulong unchecked unsafe ushort var "; var JSCRIPT_KEYWORDS = COMMON_KEYWORDS + "debugger eval export function get null set undefined var with " + "Infinity NaN "; var PERL_KEYWORDS = "caller delete die do dump elsif eval exit foreach for " + "goto if import last local my next no our print package redo require " + "sub undef unless until use wantarray while BEGIN END "; var PYTHON_KEYWORDS = FLOW_CONTROL_KEYWORDS + "and as assert class def del " + "elif except exec finally from global import in is lambda " + "nonlocal not or pass print raise try with yield " + "False True None "; var RUBY_KEYWORDS = FLOW_CONTROL_KEYWORDS + "alias and begin case class def" + " defined elsif end ensure false in module next nil not or redo rescue " + "retry self super then true undef unless until when yield BEGIN END "; var SH_KEYWORDS = FLOW_CONTROL_KEYWORDS + "case done elif esac eval fi " + "function in local set then until "; var ALL_KEYWORDS = (CPP_KEYWORDS + CSHARP_KEYWORDS + JSCRIPT_KEYWORDS + PERL_KEYWORDS + PYTHON_KEYWORDS + RUBY_KEYWORDS + SH_KEYWORDS); var PR_STRING = 'str'; var PR_KEYWORD = 'kwd'; var PR_COMMENT = 'com'; var PR_TYPE = 'typ'; var PR_LITERAL = 'lit'; var PR_PUNCTUATION = 'pun'; var PR_PLAIN = 'pln'; var PR_TAG = 'tag'; var PR_DECLARATION = 'dec'; var PR_SOURCE = 'src'; var PR_ATTRIB_NAME = 'atn'; var PR_ATTRIB_VALUE = 'atv'; var PR_NOCODE = 'nocode'; function isWordChar(ch) { return (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z'); } function spliceArrayInto(inserted, container, containerPosition, countReplaced) { inserted.unshift(containerPosition, countReplaced || 0); try { container.splice.apply(container, inserted); } finally { inserted.splice(0, 2); } } var REGEXP_PRECEDER_PATTERN = function() { var preceders = ["!", "!=", "!==", "#", "%", "%=", "&", "&&", "&&=", "&=", "(", "*", "*=", "+=", ",", "-=", "->", "/", "/=", ":", "::", ";", "<", "<<", "<<=", "<=", "=", "==", "===", ">", ">=", ">>", ">>=", ">>>", ">>>=", "?", "@", "[", "^", "^=", "^^", "^^=", "{", "|", "|=", "||", "||=", "~", "break", "case", "continue", "delete", "do", "else", "finally", "instanceof", "return", "throw", "try", "typeof"]; var pattern = '(?:' + '(?:(?:^|[^0-9.])\\.{1,3})|' + '(?:(?:^|[^\\+])\\+)|' + '(?:(?:^|[^\\-])-)'; for (var i = 0; i < preceders.length; ++i) { var preceder = preceders[i]; if (isWordChar(preceder.charAt(0))) { pattern += '|\\b' + preceder; } else { pattern += '|' + preceder.replace(/([^=<>:&])/g, '\\$1'); } } pattern += '|^)\\s*$'; return new RegExp(pattern); } (); var pr_amp = /&/g; var pr_lt = /</g; var pr_gt = />/g; var pr_quot = /\"/g; function attribToHtml(str) { return str.replace(pr_amp, '&amp;').replace(pr_lt, '&lt;').replace(pr_gt, '&gt;').replace(pr_quot, '&quot;'); } function textToHtml(str) { return str.replace(pr_amp, '&amp;').replace(pr_lt, '&lt;').replace(pr_gt, '&gt;'); } var pr_ltEnt = /&lt;/g; var pr_gtEnt = /&gt;/g; var pr_aposEnt = /&apos;/g; var pr_quotEnt = /&quot;/g; var pr_ampEnt = /&amp;/g; var pr_nbspEnt = /&nbsp;/g; function htmlToText(html) { var pos = html.indexOf('&'); if (pos < 0) { return html; } for (--pos; (pos = html.indexOf('&#', pos + 1)) >= 0; ) { var end = html.indexOf(';', pos); if (end >= 0) { var num = html.substring(pos + 3, end); var radix = 10; if (num && num.charAt(0) === 'x') { num = num.substring(1); radix = 16; } var codePoint = parseInt(num, radix); if (!isNaN(codePoint)) { html = (html.substring(0, pos) + String.fromCharCode(codePoint) + html.substring(end + 1)); } } } return html.replace(pr_ltEnt, '<').replace(pr_gtEnt, '>').replace(pr_aposEnt, "'").replace(pr_quotEnt, '"').replace(pr_ampEnt, '&').replace(pr_nbspEnt, ' '); } function isRawContent(node) { return 'XMP' === node.tagName; } function normalizedHtml(node, out) { switch (node.nodeType) { case 1: var name = node.tagName.toLowerCase(); out.push('<', name); for (var i = 0; i < node.attributes.length; ++i) { var attr = node.attributes[i]; if (!attr.specified) { continue; } out.push(' '); normalizedHtml(attr, out); } out.push('>'); for (var child = node.firstChild; child; child = child.nextSibling) { normalizedHtml(child, out); } if (node.firstChild || !/^(?:br|link|img)$/.test(name)) { out.push('<\/', name, '>'); } break; case 2: out.push(node.name.toLowerCase(), '="', attribToHtml(node.value), '"'); break; case 3: case 4: out.push(textToHtml(node.nodeValue)); break; } } var PR_innerHtmlWorks = null; function getInnerHtml(node) { if (null === PR_innerHtmlWorks) { var testNode = document.createElement('PRE'); testNode.appendChild(document.createTextNode('<!DOCTYPE foo PUBLIC "foo bar">\n<foo />')); PR_innerHtmlWorks = !/</.test(testNode.innerHTML); } if (PR_innerHtmlWorks) { var content = node.innerHTML; if (isRawContent(node)) { content = textToHtml(content); } return content; } var out = []; for (var child = node.firstChild; child; child = child.nextSibling) { normalizedHtml(child, out); } return out.join(''); } function makeTabExpander(tabWidth) { var SPACES = '                '; var charInLine = 0; return function(plainText) { var out = null; var pos = 0; for (var i = 0, n = plainText.length; i < n; ++i) { var ch = plainText.charAt(i); switch (ch) { case '\t': if (!out) { out = []; } out.push(plainText.substring(pos, i)); var nSpaces = tabWidth - (charInLine % tabWidth); charInLine += nSpaces; for (; nSpaces >= 0; nSpaces -= SPACES.length) { out.push(SPACES.substring(0, nSpaces)); } pos = i + 1; break; case '\n': charInLine = 0; break; default: ++charInLine; } } if (!out) { return plainText; } out.push(plainText.substring(pos)); return out.join(''); }; } var pr_chunkPattern = /(?:[^<]+|<!--[\s\S]*?-->|<!\[CDATA\[([\s\S]*?)\]\]>|<\/?[a-zA-Z][^>]*>|<)/g; var pr_commentPrefix = /^<!--/; var pr_cdataPrefix = /^<\[CDATA\[/; var pr_brPrefix = /^<br\b/i; var pr_tagNameRe = /^<(\/?)([a-zA-Z]+)/; function extractTags(s) { var matches = s.match(pr_chunkPattern); var sourceBuf = []; var sourceBufLen = 0; var extractedTags = []; if (matches) { for (var i = 0, n = matches.length; i < n; ++i) { var match = matches[i]; if (match.length > 1 && match.charAt(0) === '<') { if (pr_commentPrefix.test(match)) { continue; } if (pr_cdataPrefix.test(match)) { sourceBuf.push(match.substring(9, match.length - 3)); sourceBufLen += match.length - 12; } else if (pr_brPrefix.test(match)) { sourceBuf.push('\n'); ++sourceBufLen; } else { if (match.indexOf(PR_NOCODE) >= 0 && isNoCodeTag(match)) { var name = match.match(pr_tagNameRe)[2]; var depth = 1; end_tag_loop: for (var j = i + 1; j < n; ++j) { var name2 = matches[j].match(pr_tagNameRe); if (name2 && name2[2] === name) { if (name2[1] === '/') { if (--depth === 0) { break end_tag_loop; } } else { ++depth; } } } if (j < n) { extractedTags.push(sourceBufLen, matches.slice(i, j + 1).join('')); i = j; } else { extractedTags.push(sourceBufLen, match); } } else { extractedTags.push(sourceBufLen, match); } } } else { var literalText = htmlToText(match); sourceBuf.push(literalText); sourceBufLen += literalText.length; } } } return { source: sourceBuf.join(''), tags: extractedTags }; } function isNoCodeTag(tag) { return !!tag.replace(/\s(\w+)\s*=\s*(?:\"([^\"]*)\"|'([^\']*)'|(\S+))/g, ' $1="$2$3$4"').match(/[cC][lL][aA][sS][sS]=\"[^\"]*\bnocode\b/); } function createSimpleLexer(shortcutStylePatterns, fallthroughStylePatterns) { var shortcuts = {}; (function() { var allPatterns = shortcutStylePatterns.concat(fallthroughStylePatterns); for (var i = allPatterns.length; --i >= 0; ) { var patternParts = allPatterns[i]; var shortcutChars = patternParts[3]; if (shortcutChars) { for (var c = shortcutChars.length; --c >= 0; ) { shortcuts[shortcutChars.charAt(c)] = patternParts; } } } })(); var nPatterns = fallthroughStylePatterns.length; var notWs = /\S/; return function(sourceCode, opt_basePos) { opt_basePos = opt_basePos || 0; var decorations = [opt_basePos, PR_PLAIN]; var lastToken = ''; var pos = 0; var tail = sourceCode; while (tail.length) { var style; var token = null; var match; var patternParts = shortcuts[tail.charAt(0)]; if (patternParts) { match = tail.match(patternParts[1]); token = match[0]; style = patternParts[0]; } else { for (var i = 0; i < nPatterns; ++i) { patternParts = fallthroughStylePatterns[i]; var contextPattern = patternParts[2]; if (contextPattern && !contextPattern.test(lastToken)) { continue; } match = tail.match(patternParts[1]); if (match) { token = match[0]; style = patternParts[0]; break; } } if (!token) { style = PR_PLAIN; token = tail.substring(0, 1); } } decorations.push(opt_basePos + pos, style); pos += token.length; tail = tail.substring(token.length); if (style !== PR_COMMENT && notWs.test(token)) { lastToken = token; } } return decorations; }; } var PR_MARKUP_LEXER = createSimpleLexer([], [[PR_PLAIN, /^[^<]+/, null], [PR_DECLARATION, /^<!\w[^>]*(?:>|$)/, null], [PR_COMMENT, /^<!--[\s\S]*?(?:-->|$)/, null], [PR_SOURCE, /^<\?[\s\S]*?(?:\?>|$)/, null], [PR_SOURCE, /^<%[\s\S]*?(?:%>|$)/, null], [PR_SOURCE, /^<(script|style|xmp)\b[^>]*>[\s\S]*?<\/\1\b[^>]*>/i, null], [PR_TAG, /^<\/?\w[^<>]*>/, null]]); var PR_SOURCE_CHUNK_PARTS = /^(<[^>]*>)([\s\S]*)(<\/[^>]*>)$/; function tokenizeMarkup(source) { var decorations = PR_MARKUP_LEXER(source); for (var i = 0; i < decorations.length; i += 2) { if (decorations[i + 1] === PR_SOURCE) { var start, end; start = decorations[i]; end = i + 2 < decorations.length ? decorations[i + 2] : source.length; var sourceChunk = source.substring(start, end); var match = sourceChunk.match(PR_SOURCE_CHUNK_PARTS); if (match) { decorations.splice(i, 2, start, PR_TAG, start + match[1].length, PR_SOURCE, start + match[1].length + (match[2] || '').length, PR_TAG); } } } return decorations; } var PR_TAG_LEXER = createSimpleLexer([[PR_ATTRIB_VALUE, /^\'[^\']*(?:\'|$)/, null, "'"], [PR_ATTRIB_VALUE, /^\"[^\"]*(?:\"|$)/, null, '"'], [PR_PUNCTUATION, /^[<>\/=]+/, null, '<>/=']], [[PR_TAG, /^[\w:\-]+/, /^</], [PR_ATTRIB_VALUE, /^[\w\-]+/, /^=/], [PR_ATTRIB_NAME, /^[\w:\-]+/, null], [PR_PLAIN, /^\s+/, null, ' \t\r\n']]); function splitTagAttributes(source, decorations) { for (var i = 0; i < decorations.length; i += 2) { var style = decorations[i + 1]; if (style === PR_TAG) { var start, end; start = decorations[i]; end = i + 2 < decorations.length ? decorations[i + 2] : source.length; var chunk = source.substring(start, end); var subDecorations = PR_TAG_LEXER(chunk, start); spliceArrayInto(subDecorations, decorations, i, 2); i += subDecorations.length - 2; } } return decorations; } function sourceDecorator(options) { var shortcutStylePatterns = [], fallthroughStylePatterns = []; if (options.tripleQuotedStrings) { shortcutStylePatterns.push([PR_STRING, /^(?:\'\'\'(?:[^\'\\]|\\[\s\S]|\'{1,2}(?=[^\']))*(?:\'\'\'|$)|\"\"\"(?:[^\"\\]|\\[\s\S]|\"{1,2}(?=[^\"]))*(?:\"\"\"|$)|\'(?:[^\\\']|\\[\s\S])*(?:\'|$)|\"(?:[^\\\"]|\\[\s\S])*(?:\"|$))/, null, '\'"']); } else if (options.multiLineStrings) { shortcutStylePatterns.push([PR_STRING, /^(?:\'(?:[^\\\']|\\[\s\S])*(?:\'|$)|\"(?:[^\\\"]|\\[\s\S])*(?:\"|$)|\`(?:[^\\\`]|\\[\s\S])*(?:\`|$))/, null, '\'"`']); } else { shortcutStylePatterns.push([PR_STRING, /^(?:\'(?:[^\\\'\r\n]|\\.)*(?:\'|$)|\"(?:[^\\\"\r\n]|\\.)*(?:\"|$))/, null, '"\'']); } fallthroughStylePatterns.push([PR_PLAIN, /^(?:[^\'\"\`\/\#]+)/, null, ' \r\n']); if (options.hashComments) { shortcutStylePatterns.push([PR_COMMENT, /^#[^\r\n]*/, null, '#']); } if (options.cStyleComments) { fallthroughStylePatterns.push([PR_COMMENT, /^\/\/[^\r\n]*/, null]); fallthroughStylePatterns.push([PR_COMMENT, /^\/\*[\s\S]*?(?:\*\/|$)/, null]); } if (options.regexLiterals) { var REGEX_LITERAL = ('^/(?=[^/*])' + '(?:[^/\\x5B\\x5C]' + '|\\x5C[\\s\\S]' + '|\\x5B(?:[^\\x5C\\x5D]|\\x5C[\\s\\S])*(?:\\x5D|$))+' + '(?:/|$)'); fallthroughStylePatterns.push([PR_STRING, new RegExp(REGEX_LITERAL), REGEXP_PRECEDER_PATTERN]); } var keywords = wordSet(options.keywords); options = null; var splitStringAndCommentTokens = createSimpleLexer(shortcutStylePatterns, fallthroughStylePatterns); var styleLiteralIdentifierPuncRecognizer = createSimpleLexer([], [[PR_PLAIN, /^\s+/, null, ' \r\n'], [PR_PLAIN, /^[a-z_$@][a-z_$@0-9]*/i, null], [PR_LITERAL, /^0x[a-f0-9]+[a-z]/i, null], [PR_LITERAL, /^(?:\d(?:_\d+)*\d*(?:\.\d*)?|\.\d+)(?:e[+\-]?\d+)?[a-z]*/i, null, '123456789'], [PR_PUNCTUATION, /^[^\s\w\.$@]+/, null]]); function splitNonStringNonCommentTokens(source, decorations) { for (var i = 0; i < decorations.length; i += 2) { var style = decorations[i + 1]; if (style === PR_PLAIN) { var start, end, chunk, subDecs; start = decorations[i]; end = i + 2 < decorations.length ? decorations[i + 2] : source.length; chunk = source.substring(start, end); subDecs = styleLiteralIdentifierPuncRecognizer(chunk, start); for (var j = 0, m = subDecs.length; j < m; j += 2) { var subStyle = subDecs[j + 1]; if (subStyle === PR_PLAIN) { var subStart = subDecs[j]; var subEnd = j + 2 < m ? subDecs[j + 2] : chunk.length; var token = source.substring(subStart, subEnd); if (token === '.') { subDecs[j + 1] = PR_PUNCTUATION; } else if (token in keywords) { subDecs[j + 1] = PR_KEYWORD; } else if (/^@?[A-Z][A-Z$]*[a-z][A-Za-z$]*$/.test(token)) { subDecs[j + 1] = token.charAt(0) === '@' ? PR_LITERAL : PR_TYPE; } } } spliceArrayInto(subDecs, decorations, i, 2); i += subDecs.length - 2; } } return decorations; } return function(sourceCode) { var decorations = splitStringAndCommentTokens(sourceCode); decorations = splitNonStringNonCommentTokens(sourceCode, decorations); return decorations; }; } var decorateSource = sourceDecorator({ keywords: ALL_KEYWORDS, hashComments: true, cStyleComments: true, multiLineStrings: true, regexLiterals: true }); function splitSourceNodes(source, decorations) { for (var i = 0; i < decorations.length; i += 2) { var style = decorations[i + 1]; if (style === PR_SOURCE) { var start, end; start = decorations[i]; end = i + 2 < decorations.length ? decorations[i + 2] : source.length; var subDecorations = decorateSource(source.substring(start, end)); for (var j = 0, m = subDecorations.length; j < m; j += 2) { subDecorations[j] += start; } spliceArrayInto(subDecorations, decorations, i, 2); i += subDecorations.length - 2; } } return decorations; } function splitSourceAttributes(source, decorations) { var nextValueIsSource = false; for (var i = 0; i < decorations.length; i += 2) { var style = decorations[i + 1]; var start, end; if (style === PR_ATTRIB_NAME) { start = decorations[i]; end = i + 2 < decorations.length ? decorations[i + 2] : source.length; nextValueIsSource = /^on|^style$/i.test(source.substring(start, end)); } else if (style === PR_ATTRIB_VALUE) { if (nextValueIsSource) { start = decorations[i]; end = i + 2 < decorations.length ? decorations[i + 2] : source.length; var attribValue = source.substring(start, end); var attribLen = attribValue.length; var quoted = (attribLen >= 2 && /^[\"\']/.test(attribValue) && attribValue.charAt(0) === attribValue.charAt(attribLen - 1)); var attribSource; var attribSourceStart; var attribSourceEnd; if (quoted) { attribSourceStart = start + 1; attribSourceEnd = end - 1; attribSource = attribValue; } else { attribSourceStart = start + 1; attribSourceEnd = end - 1; attribSource = attribValue.substring(1, attribValue.length - 1); } var attribSourceDecorations = decorateSource(attribSource); for (var j = 0, m = attribSourceDecorations.length; j < m; j += 2) { attribSourceDecorations[j] += attribSourceStart; } if (quoted) { attribSourceDecorations.push(attribSourceEnd, PR_ATTRIB_VALUE); spliceArrayInto(attribSourceDecorations, decorations, i + 2, 0); } else { spliceArrayInto(attribSourceDecorations, decorations, i, 2); } } nextValueIsSource = false; } } return decorations; } function decorateMarkup(sourceCode) { var decorations = tokenizeMarkup(sourceCode); decorations = splitTagAttributes(sourceCode, decorations); decorations = splitSourceNodes(sourceCode, decorations); decorations = splitSourceAttributes(sourceCode, decorations); return decorations; } function recombineTagsAndDecorations(sourceText, extractedTags, decorations) { var html = []; var outputIdx = 0; var openDecoration = null; var currentDecoration = null; var tagPos = 0; var decPos = 0; var tabExpander = makeTabExpander(PR_TAB_WIDTH); var adjacentSpaceRe = /([\r\n ]) /g; var startOrSpaceRe = /(^| ) /gm; var newlineRe = /\r\n?|\n/g; var trailingSpaceRe = /[ \r\n]$/; var lastWasSpace = true; function emitTextUpTo(sourceIdx) { if (sourceIdx > outputIdx) { if (openDecoration && openDecoration !== currentDecoration) { html.push('</span>'); openDecoration = null; } if (!openDecoration && currentDecoration) { openDecoration = currentDecoration; html.push('<span class="', openDecoration, '">'); } var htmlChunk = textToHtml(tabExpander(sourceText.substring(outputIdx, sourceIdx))).replace(lastWasSpace ? startOrSpaceRe : adjacentSpaceRe, '$1&nbsp;'); lastWasSpace = trailingSpaceRe.test(htmlChunk); html.push(htmlChunk.replace(newlineRe, '<br />')); outputIdx = sourceIdx; } } while (true) { var outputTag; if (tagPos < extractedTags.length) { if (decPos < decorations.length) { outputTag = extractedTags[tagPos] <= decorations[decPos]; } else { outputTag = true; } } else { outputTag = false; } if (outputTag) { emitTextUpTo(extractedTags[tagPos]); if (openDecoration) { html.push('</span>'); openDecoration = null; } html.push(extractedTags[tagPos + 1]); tagPos += 2; } else if (decPos < decorations.length) { emitTextUpTo(decorations[decPos]); currentDecoration = decorations[decPos + 1]; decPos += 2; } else { break; } } emitTextUpTo(sourceText.length); if (openDecoration) { html.push('</span>'); } return html.join(''); } var langHandlerRegistry = {}; function registerLangHandler(handler, fileExtensions) { for (var i = fileExtensions.length; --i >= 0; ) { var ext = fileExtensions[i]; if (!langHandlerRegistry.hasOwnProperty(ext)) { langHandlerRegistry[ext] = handler; } else if ('console' in window) { console.log('cannot override language handler %s', ext); } } } registerLangHandler(decorateSource, ['default-code']); registerLangHandler(decorateMarkup, ['default-markup', 'html', 'htm', 'xhtml', 'xml', 'xsl']); registerLangHandler(sourceDecorator({ keywords: CPP_KEYWORDS, hashComments: true, cStyleComments: true }), ['c', 'cc', 'cpp', 'cs', 'cxx', 'cyc']); registerLangHandler(sourceDecorator({ keywords: JAVA_KEYWORDS, cStyleComments: true }), ['java']); registerLangHandler(sourceDecorator({ keywords: SH_KEYWORDS, hashComments: true, multiLineStrings: true }), ['bsh', 'csh', 'sh']); registerLangHandler(sourceDecorator({ keywords: PYTHON_KEYWORDS, hashComments: true, multiLineStrings: true, tripleQuotedStrings: true }), ['cv', 'py']); registerLangHandler(sourceDecorator({ keywords: PERL_KEYWORDS, hashComments: true, multiLineStrings: true, regexLiterals: true }), ['perl', 'pl', 'pm']); registerLangHandler(sourceDecorator({ keywords: RUBY_KEYWORDS, hashComments: true, multiLineStrings: true, regexLiterals: true }), ['rb']); registerLangHandler(sourceDecorator({ keywords: JSCRIPT_KEYWORDS, cStyleComments: true, regexLiterals: true }), ['js']); function prettyPrintOne(sourceCodeHtml, opt_langExtension) { try { var sourceAndExtractedTags = extractTags(sourceCodeHtml); var source = sourceAndExtractedTags.source; var extractedTags = sourceAndExtractedTags.tags; if (!langHandlerRegistry.hasOwnProperty(opt_langExtension)) { opt_langExtension = /^\s*</.test(source) ? 'default-markup' : 'default-code'; } var decorations = langHandlerRegistry[opt_langExtension].call({}, source); return recombineTagsAndDecorations(source, extractedTags, decorations); } catch (e) { if ('console' in window) { console.log(e); console.trace(); } return sourceCodeHtml; } } function prettyPrint(opt_whenDone) { var isIE6 = _pr_isIE6(); var codeSegments = [document.getElementsByTagName('pre'), document.getElementsByTagName('code'), document.getElementsByTagName('xmp')]; var elements = []; for (var i = 0; i < codeSegments.length; ++i) { for (var j = 0; j < codeSegments[i].length; ++j) { elements.push(codeSegments[i][j]); } } codeSegments = null; var k = 0; function doWork() { var endTime = (PR_SHOULD_USE_CONTINUATION ? new Date().getTime() + 250 : Infinity); for (; k < elements.length && new Date().getTime() < endTime; k++) { var cs = elements[k]; if (cs.className && cs.className.indexOf('prettyprint') >= 0) { var langExtension = cs.className.match(/\blang-(\w+)\b/); if (langExtension) { langExtension = langExtension[1]; } var nested = false; for (var p = cs.parentNode; p; p = p.parentNode) { if ((p.tagName === 'pre' || p.tagName === 'code' || p.tagName === 'xmp') && p.className && p.className.indexOf('prettyprint') >= 0) { nested = true; break; } } if (!nested) { var content = getInnerHtml(cs); content = content.replace(/(?:\r\n?|\n)$/, ''); var newContent = prettyPrintOne(content, langExtension); if (!isRawContent(cs)) { cs.innerHTML = newContent; } else { var pre = document.createElement('PRE'); for (var i = 0; i < cs.attributes.length; ++i) { var a = cs.attributes[i]; if (a.specified) { var aname = a.name.toLowerCase(); if (aname === 'class') { pre.className = a.value; } else { pre.setAttribute(a.name, a.value); } } } pre.innerHTML = newContent; cs.parentNode.replaceChild(pre, cs); cs = pre; } if (isIE6 && cs.tagName === 'PRE') { var lineBreaks = cs.getElementsByTagName('br'); for (var j = lineBreaks.length; --j >= 0; ) { var lineBreak = lineBreaks[j]; lineBreak.parentNode.replaceChild(document.createTextNode('\r\n'), lineBreak); } } } } } if (k < elements.length) { setTimeout(doWork, 250); } else if (opt_whenDone) { opt_whenDone(); } } doWork(); } window['PR_normalizedHtml'] = normalizedHtml; window['prettyPrintOne'] = prettyPrintOne; window['prettyPrint'] = prettyPrint; window['PR'] = { 'createSimpleLexer': createSimpleLexer, 'registerLangHandler': registerLangHandler, 'sourceDecorator': sourceDecorator, 'PR_ATTRIB_NAME': PR_ATTRIB_NAME, 'PR_ATTRIB_VALUE': PR_ATTRIB_VALUE, 'PR_COMMENT': PR_COMMENT, 'PR_DECLARATION': PR_DECLARATION, 'PR_KEYWORD': PR_KEYWORD, 'PR_LITERAL': PR_LITERAL, 'PR_NOCODE': PR_NOCODE, 'PR_PLAIN': PR_PLAIN, 'PR_PUNCTUATION': PR_PUNCTUATION, 'PR_SOURCE': PR_SOURCE, 'PR_STRING': PR_STRING, 'PR_TAG': PR_TAG, 'PR_TYPE': PR_TYPE }; })();
