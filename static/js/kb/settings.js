//-------------------------------
// 設定 > 管理成員 JS
//-------------------------------
if (is_owner){
    $("#mgmt-member").tagit({
        showAutocompleteOnFocus: false,
        singleField: true,
        caseSensitive: true,
        allowDuplicates: false,
        readOnly: true,
        onTagClicked: function(event, ui) {
            $(".member-tooltip").off("click");
            $(".member-tooltip").click(function(){
                mgmtMemberInput(ui.tag.context.firstChild.data);
            }); 
        }
    });
    $("#mgmt-member").data("ui-tagit").tagInput.addClass('uk-input');
    $('#mgmt-member > .tagit-choice').addClass("mgmt-member-option");
    $("#mgmt-member > li").append('<div class="member-tooltip uk-inline" style="cursor: pointer;">從專案移除</div>');
    // 刪除成員的選項
    $('.mgmt-member-option').mousedown(function(){
        var pos = $(this).position();
        $(this).find('.member-tooltip').css('top', (pos.top)+10 + 'px').fadeIn();
        $('.mgmt-member-option').mouseleave(function(){
            $(this).find('.member-tooltip').fadeOut();
        });
    });
}

//-------------------------------
// 設定 > 新增成員 JS
//-------------------------------
$("#add-member").tagit({
    fieldName: "add-members",
    autocomplete: {delay: 0, minLength: 4, source: allUserID},
    showAutocompleteOnFocus: false,
    singleField: true,
    tagLimit: null,
    caseSensitive: true,
    allowDuplicates: false,
});
$("#add-member").data("ui-tagit").tagInput.addClass('uk-input uk-margin-small-left');
$("#add-member").data("ui-tagit").tagInput.attr('placeholder', '請輸入欲新增的帳號');
$("#add-member").data("ui-tagit").tagInput.attr('required');
$("#add-member").data("ui-tagit").tagInput.attr('id', 'members-to-add');
$("#add-member").data("ui-tagit").tagInput.attr('name', 'members-to-addowner');
$("#add-member").data("ui-tagit").tagInput.attr('type', 'text');
// 新增成員輸入事件
$("#add-member").tagit({
    afterTagAdded: function (event, ui) {
        addMemberInput(ui.tagLabel, "added");
        $("#proj-member-list").append('<li class="tagit-choice ui-widget-content ui-state-default ui-corner-all tagit-choice-read-only"><span class="tagit-label">' + ui.tagLabel + '</span><input type="hidden" value="' + ui.tagLabel + '" name="tags" class="tagit-hidden-field"></li>')
        $("#proj-member-list > .tagit-new").remove();
    },
    afterTagRemoved: function (event, ui) {
        addMemberInput(ui.tagLabel, "removed");
        $("li:contains('" + ui.tagLabel +"')").remove();
        $("#proj-member-list > .tagit-new").remove();
    }
});

//-------------------------------
// 設定 > 刪除專案 X按鈕功能
//-------------------------------
$("#settings-form").submit( function (e) {
    e.preventDefault();
});
$("#delete-project").click( function(){
    $("#page-spinner").fadeIn();
    $("#spinner-bg").fadeIn();
    $.ajax({
        method: "GET",
        url: "/board/deleteProject/",
        success: function(responseText){
            document.write(responseText);
        },
    });
});

// 點擊側邊選單出現spinner
$(".list").click( function(){
    $("#page-spinner").fadeIn();
    $("#spinner-bg").fadeIn();
})
// 阻擋enter鍵送出表單
$(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
});

//-------------------------------
// function
//-------------------------------
// 新增成員 輸入或刪除成員的動作
function addMemberInput(tagLabel, state){
    var htmlClass = new String();
    var htmlText = new String();
    if (allUserID.includes(tagLabel)){
        if (projUserID.includes(tagLabel)){
            htmlClass = "alert";
            htmlText = "已經是本專案成員";
        }
        else if (state == "removed"){
            removeMember(tagLabel);
            htmlClass = "removed-hint";
            htmlText = "已移除";
        }
        else if (state == "added"){
            addMember(tagLabel);
            htmlClass = "added-hint";
            htmlText = "已加入專案";
        }
    }
    else {
        htmlClass = "alert";
        htmlText = "無此用戶";
    }

    html = "<p class='" 
        + htmlClass 
        + " noto-light uk-inline uk-text-small uk-margin-remove uk-margin-left'" 
        + " style='color: #139c91; display: none;'>" 
        + tagLabel + " " + htmlText +"</p>";
    $(html).insertBefore("#add-member").fadeIn();
    setTimeout(function(){
        $("." + htmlClass).fadeOut(function(){$(this).remove();});
    }, 2000)
}

// http post至後端
function addMember(tagLabel){
    $.ajax({
        method: "POST",
        url: "/board/addMember/",
        data: {
            csrfmiddlewaretoken: csrftoken,
            "member-to-add": tagLabel
        }
    });
}
function removeMember(tagLabel){
    $.ajax({
       method: "POST",
       url: "/board/deleteMember/",
       data: {
            csrfmiddlewaretoken: csrftoken,
            "member-to-delete": tagLabel
       }
    });
}

// 管理成員 輸入或刪除成員的動作
function mgmtMemberInput(context){
    if (context != "{{ owner }}"){
        $.ajax({
            method: "POST",
            url: "/board/deleteMember/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                "member-to-delete": context
            },
            success: function(data){
                $("li:contains('" + context +"')").remove();
                html = "<p class='deleted" 
                + " noto-light uk-inline uk-text-small uk-margin-remove uk-margin-left'" 
                + " style='color: #139c91; display: none;'>" 
                + context + " 已踢出專案</p>";
                insertDelAlert(html);
            }
        });
        
    }
    else {
        html = "<p class='deleted" 
        + " noto-light uk-inline uk-text-small uk-margin-remove uk-margin-left'" 
        + " style='color: #c44d58; display: none;'>" 
        + context + " 是管理員，不能移除</p>";
        insertDelAlert(html);
    }


}

function insertDelAlert(html){
    $(html).insertBefore("#mgmt-member").fadeIn();
    setTimeout(function(){
        $(".deleted").fadeOut(function(){$(this).remove();});
    }, 2000)
}

//-------------------------------
// 帳號設定
//-------------------------------
$("#account-settings-form").submit( function(e){
    e.preventDefault();
});
$("#rename").click(function(e){
    newname = $("input[name=newname]").val();
    $.ajax({
        method: "POST",
        url: "/rename/",
        data: {
            csrfmiddlewaretoken:csrftoken,
            "newname": newname
        }  
    }).done(function(data){
        html = "<div class='rename-success" 
            + " noto-light uk-inline uk-text-small uk-margin-remove uk-margin-left'" 
            + " style='color: #139c91; display: none;'>" 
            + "   已變更</div>";
        $(html).insertAfter("#rename-title").fadeIn();
        setTimeout(function(){
            $(".rename-success").fadeOut(function(){$(this).remove();});
        }, 2000)
        $("#name").text(newname);
    });

});
