var colorArray = ['#556270', '#4ecdc4', '#c7f464', '#ff6b6b', '#c44d58'];
var textColor = ['white','black','black','white','white'];

var projectMember = new Array();  // 專案成員陣列
var projectAttr = new Array();  // 專案欄位
var taskCard = new Array();  // 專案所有卡片與欄位
// [異步] 取得專案資料JSON
$.getJSON("/KanbanProjJSON/", function(projectData){
    for (var i = 0 ; i < projectData['members'].length ;i++){
        projectMember.push({id: i, name: projectData['members'][i]}); // [{ id: 1, name: "Andrew Fuller"},...]
    }
    for (var i = 0 ; i < projectData['attr'].length ;i++){
        var colName = projectData['attr'][i];
        if (colName == "progress"){
            // [{ text: "...", iconClassName: "..." dataField: "..." , maxItems: 5},...]
            projectAttr.push({text: colName, dataField: colName, iconClassName: "jqx-icon-plus-alt", maxItems: 5});
        }
        else{
            projectAttr.push({text: colName, dataField: colName, iconClassName: "jqx-icon-plus-alt"});
        }


        if (isEmpty(projectData['tasks'])){
            taskCard = [{}];
        }
        else{
            for (var j = 0; j < projectData['columns'][colName].length ; j++){
                taskID = projectData['columns'][colName][j];
                // if(taskID == undefined){
                //     taskCard = [{}];
                // }
                taskContent = projectData['tasks'][taskID]["content"];
                taskOwner = projectData['tasks'][taskID]["owner"];
                taskColor = projectData['tasks'][taskID]["color"];
                taskCard.push({ id: taskID, state: colName, label: taskContent, tags: taskOwner, hex: taskColor });
            }
        }
    }

    $(document).ready(mainPage());  // jQuery
})
// END [異步] 取得專案資料JSON


// START 主要看板JS
function mainPage () {

    var color = d3.scaleOrdinal()
                .range(colorArray); 

    for (var i = 0; i < colorArray.length; i++) {
        d3.select("div")            
            .attr('style', function (d) {
            return 'background-color: ' + color(i);
        });
    }

    var fields = [// 資料型態
             { name: "id", type: "string" },
             { name: "status", map: "state", type: "string" },
             { name: "text", map: "label", type: "string" },
             { name: "tags", type: "string" },
             { name: "color", map: "hex", type: "string" },
             { name: "resourceId", type: "number" }
    ];

    var source =
     {
         localData: taskCard,
         dataType: "array",
         dataFields: fields
     };
    var dataAdapter = new $.jqx.dataAdapter(source);

    var resourcesAdapterFunc = function () {
        var resourcesSource =
        {
            localData: projectMember, // 成員
            dataType: "array",
            dataFields: [// 資料型態
                 { name: "id", type: "number" },
                 { name: "name", type: "string" },
                 { name: "image", type: "string" },
                 { name: "common", type: "boolean" }
            ]
        };
        var resourcesDataAdapter = new $.jqx.dataAdapter(resourcesSource);
        return resourcesDataAdapter;
    }
    
    // 畫出看板
    $('#kanban').jqxKanban({
        resources: resourcesAdapterFunc(),
        source: dataAdapter,
        // 自訂Task卡片物件的模板
        template: "<div class='jqx-kanban-item'>"
        + "<div class='jqx-kanban-item-color-status'></div>"
        + "<div class='jqx-icon jqx-icon-close jqx-kanban-item-template-content jqx-kanban-template-icon'></div>"
        + "<div class='jqx-kanban-item-text'></div>"
        + "<div class='jqx-kanban-item-footer'></div>"
        + "<ul class='uk-iconnav uk-position-bottom-right uk-margin-right uk-margin-small-bottom'>"
        + "<li><div uk-icon='pencil'></div></li>"
        + "<li><div uk-icon='close' class='close'></div></li>"
        + "</ul>"
        + "</div>",
        theme: "light",
        height: "494px",
        width: '800px',
        // 定義卡片樣式
        itemRenderer: function(element, item, resource){
                $(element)
                    .css('background', item.color)// Task卡片底色
                    .css('border-style', 'none')
                    .css('border-radius', '4px')
                    .css('margin-top', '12px')
                    .css('margin-bottom', '12px')
                    // 拖曳陰影效果
                    .mouseup(function (e) {// 滑鼠按下
                        $(e.target).closest('.jqx-kanban-item').css('box-shadow', '0 2px 4px 0 rgba(0, 0, 0, 0.1), 0 2px 5px 0 rgba(0, 0, 0, 0.089)');
                    })
                    .mousedown(function(e) {// 放開滑鼠
                        $(e.target).closest('.jqx-kanban-item').css('box-shadow', '0 8px 20px 5px rgba(0, 0, 0, 0.25)');
                    });
                $(element).find(".jqx-kanban-item-footer").css('border-top-color', item.color);// 卡片上色
                $(element).find(".jqx-kanban-item-text").css('color', textColor[colorArray.indexOf(item.color)]);// 卡片文字顏色
        },
        // 定義看板行
        columns: projectAttr,

        // 看板行標題樣式
        columnRenderer: function (element, collapsedElement, column) {
            var columnItems = $("#kanban").jqxKanban('getColumnItems', column.dataField).length;
            element.find(".jqx-kanban-column-header-title")
            .css('height', '50px')
            .css('line-height', '50px');
            if (column.dataField == "progress"){
                // update header's status.
                element.find(".jqx-kanban-column-header-title").html("<p style='line-height: 25px;'>" + column.text + "<br><x class='work-items'>" + columnItems + "/" + (column.maxItems-1) + "</x></p>");
                // update collapsed header's status.
                collapsedElement.find(".jqx-kanban-column-header-title").html(column.text);
                collapsedElement.find(".jqx-kanban-column-header-status").html("<x class='work-items'>  " + columnItems + "/" + (column.maxItems-1) + "</x>");
                // 數量滿了變成紅字
                workItems = $('.work-items');
                if (columnItems >= column.maxItems)
                    workItems.css('color', 'red');
                else
                    workItems.css('color', '');
            }
            $(".jqx-kanban-column-header-title").css('left', '-80px');
            $(".jqx-kanban-column-header-status").css('left', '-80px');
            $(".jqx-icon-plus-alt").attr("uk-toggle", "target: #new-card");
        }
    }); 
    var itemIndex = 0;// 新增卡片的編號從0開始

    // 新增Task卡片
    $('#kanban').on('columnAttrClicked', function (event) {
        var args = event.args;
        document.getElementById("card-column").value = args.column['text'];
        args.cancelToggle = true;
        if (args.attribute == "button") {
            $("#card-submit").click(function() {
                
                if (!args.column.collapsed) {
                    $('#kanban').jqxKanban('addItem', 
                    { 
                        status: document.getElementById("card-columns").value, 
                        text: document.getElementById("card-content").value, 
                        tags: document.getElementById("card-owner").value, 
                        color: document.getElementById("card-color").value
                    });
                    // 新增的Task一樣要改成自訂的樣式
                    $('.new-task > .jqx-kanban-item-text')
                    .css('color', textColor[colorArray.indexOf(inputColor)])
                    .addClass('kanban-item-text')
                    .removeClass('jqx-kanban-item-text');
                    $('.new-task > .jqx-kanban-item-color-status').remove();
                    $('.new-task').removeClass('new-task'); 
                }
            })
        }
            // args.cancelToggle = true;
            // if (!args.column.collapsed) {
            //     // 新增卡片的顏色
            //     var inputColor = color(getRandom(1,5));
            //     // 點選+號要做的事：新增卡片
            //     $('#kanban').jqxKanban('addItem', { 
            //         status: args.column.dataField, 
            //         text: "<input placeholder='Input task name here.' style='width: 96%; margin-top:2px; border-color: transparent; text-align: center; color: "+ textColor[colorArray.indexOf(inputColor)] +"; line-height:20px; height: 20px;' class='jqx-input' id='newItem" + itemIndex + "' value=''/>", 
            //         tags: "new task", 
            //         color: inputColor, 
            //         resourceId: Math.floor(Math.random() * 4), 
            //         className: "new-task" 
            //     });
            //     // 打字的地方
            //     var input =  $("#newItem" + itemIndex);
            //     input.mousedown(function (event) {
            //         event.stopPropagation();
            //     });
            //     input.mouseup(function (event) {
            //         event.stopPropagation();
            //     });
            //     input.keydown(function (event) {
            //         if (event.keyCode == 13) {
            //             $("<span>" + $(event.target).val() + "</span>").insertBefore($(event.target));
            //             $(event.target).remove();
            //         }
            //     });
            //     input.focus();
            //     itemIndex++;
                // // 新增的Task一樣要改成自訂的樣式
                // $('.new-task > .jqx-kanban-item-text')
                //     .css('color', textColor[colorArray.indexOf(inputColor)])
                //     .addClass('kanban-item-text')
                //     .removeClass('jqx-kanban-item-text');
                // $('.new-task > .jqx-kanban-item-color-status').remove();
                // $('.new-task').removeClass('new-task');  
        //     }
        // }
    });

    // 以下是把jQWidget預設樣式改掉的部分
    $('.jqx-kanban-column-header').css('height', '50px');
    $('.jqx-kanban-column-container').css('padding', '10px');
    // 這邊可以不用看，把預設Class改鰾文字才能真正居中，不知道為什麼
    $('.jqx-kanban-item-text').addClass('kanban-item-text')
    .removeClass('jqx-kanban-item-text');
    $('.jqx-kanban-item-color-status').remove();


    // 卡片OnMove
    $('#kanban').on('itemMoved', function (event) {
        var args = event.args;
        var itemId = args.itemId;
        var oldParentId = args.oldParentId;
        var newParentId = args.newParentId;
        var itemData = args.itemData;
        var oldColumn = args.oldColumn;
        var newColumn = args.newColumn;
        console.log(itemId, oldColumn["text"], newColumn["text"]);
        var src = oldColumn["text"];
        var dst = newColumn["text"];
        $.ajax({
            method: 'POST',
            url: '/board/movetask/',
            data: {
                csrfmiddlewaretoken: csrftoken,
                taskId: itemId,
                "src": src,
                "dst": dst
            },
            success: function (data) {
                 //this gets called when server returns an OK response
                 console.log("sent");
            },
            error: function (data) {
                 console.log("not sent");
            }
        })
        console.log("sent!");
    });

    for (var i = 0 ; i < taskCard.length ; i++){
        closeButton(taskCard[i]['id'], taskCard[i]['state']);
    }
}
// END 主要看板JS

/////////////////////////////////////////////////////////
//              獨立function
/////////////////////////////////////////////////////////



// get random number
function getRandom(min,max){
    return Math.floor(Math.random()*(max-min+1))+min;
}

// 把RGB轉成16進位格式
var rgbToHex = function (rgb) { 
    var a = rgb.split("(")[1].split(")")[0];
    a = a.split(",");
    var b = a.map(function(x){
        x = parseInt(x).toString(16);
        return (x.length==1) ? "0"+x : x;
    })
    b = "#"+b.join("");
    return b;
}

function closeButton (id, col){
    $("#kanban_" + id + " > ul > li >.close").click(function(){
        $.ajax({
            method: 'POST',
            url: '/board/deleteTask/',
            data: {
                csrfmiddlewaretoken: csrftoken,
                "taskId": id,
                "column": col
            },
            success: function (data) {
                 //this gets called when server returns an OK response
                 console.log("sent");
            },
            error: function (data) {
                 console.log("not sent");
            }
        })
        $("#kanban_" + id).remove();
    })
}

function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}