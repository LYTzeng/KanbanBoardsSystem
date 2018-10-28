var colorArray = ['#556270', '#4ecdc4', '#c7f464', '#ff6b6b', '#c44d58'];
var textColor = ['white','black','black','white','white'];

$(document).ready(function () {

    var color = d3.scaleOrdinal()
                .range(colorArray); 

    for (var i = 0; i < colorArray.length; i++) {
        d3.select("div")            
            .attr('style', function (d) {
            return 'background-color: ' + color(i);
        });
        }

    var fields = [
             { name: "id", type: "string" },
             { name: "status", map: "state", type: "string" },
             { name: "text", map: "label", type: "string" },
             { name: "tags", type: "string" },
             { name: "color", map: "hex", type: "string" },
             { name: "resourceId", type: "number" }
    ];
    var source =
     {
         localData: [
                  { id: "1161", state: "new", label: "SRS撰寫", tags: "SRS", hex: color(getRandom(1,5))},
                  { id: "1645", state: "work", label: "Prototyping", tags: "Prototype", hex: color(getRandom(1,5))},
                  { id: "9213", state: "new", label: "登入驗證開發與測試", tags: "登入,開發", hex: color(getRandom(1,5))},
                  { id: "6546", state: "done", label: "登入驗證設計", tags: "登入, 設計", hex: color(getRandom(1,5))},
                  { id: "9034", state: "new", label: "UI Design", tags: "UI, 設計", hex: color(getRandom(1,5))},
                  { id: "9034", state: "new", label: "資料庫設計", tags: "資料庫設計, 設計", hex: color(getRandom(1,5))},
                  { id: "9034", state: "new", label: "專案選單數計", tags: "選單, 設計", hex: color(getRandom(1,5))},
                  { id: "9034", state: "new", label: "任務管理設計", tags: "任務管理, 設計", hex: color(getRandom(1,5))},
         ],
         dataType: "array",
         dataFields: fields
     };
    var dataAdapter = new $.jqx.dataAdapter(source);
    var resourcesAdapterFunc = function () {
        var resourcesSource =
        {
            localData: [
                  { id: 0, name: "No name",  common: true },
                  { id: 1, name: "Andrew Fuller"},
                  { id: 2, name: "Janet Leverling" },
                  { id: 3, name: "Steven Buchanan"  },
                  { id: 4, name: "Nancy Davolio" },
                  { id: 5, name: "Michael Buchanan"},
                  { id: 6, name: "Margaret Buchanan"},
                  { id: 7, name: "Robert Buchanan"},
                  { id: 8, name: "Laura Buchanan"  },
                  { id: 9, name: "Laura Buchanan"  }
            ],
            dataType: "array",
            dataFields: [
                 { name: "id", type: "number" },
                 { name: "name", type: "string" },
                 { name: "image", type: "string" },
                 { name: "common", type: "boolean" }
            ]
        };
        var resourcesDataAdapter = new $.jqx.dataAdapter(resourcesSource);
        return resourcesDataAdapter;
    }

    var getIconClassName = function () {
        return "jqx-icon-plus-alt";
    }

    $('#kanban').jqxKanban({
        resources: resourcesAdapterFunc(),
        source: dataAdapter,
        theme: "light",
      
        columns: [
            { text: "TO DO", iconClassName: getIconClassName(), dataField: "new" },
            { text: "In Progress", iconClassName: getIconClassName(), dataField: "work" },
            { text: "Done", iconClassName: getIconClassName(), dataField: "done" }
        ]
    }); 
    var itemIndex = 0;
    // 新增Task
    $('#kanban').on('columnAttrClicked', function (event) {
        var args = event.args;
        if (args.attribute == "button") {
            args.cancelToggle = true;
            if (!args.column.collapsed) {
                var inputColor = color(getRandom(1,5));
                $('#kanban').jqxKanban('addItem', { status: args.column.dataField, text: "<input placeholder='Input task name here.' style='width: 96%; margin-top:2px; border-color: transparent; text-align: center; color: "+ textColor[colorArray.indexOf(inputColor)] +"; line-height:20px; height: 20px;' class='jqx-input' id='newItem" + itemIndex + "' value=''/>", tags: "new task", color: inputColor, resourceId: Math.floor(Math.random() * 4), className: "new-task" });
                var input =  $("#newItem" + itemIndex);
                input.mousedown(function (event) {
                    event.stopPropagation();
                });
                input.mouseup(function (event) {
                    event.stopPropagation();
                });

                input.keydown(function (event) {
                    if (event.keyCode == 13) {
                        $("<span>" + $(event.target).val() + "</span>").insertBefore($(event.target));
                        $(event.target).remove();
                    }
                });
                input.focus();
                itemIndex++;
                // 新增的Task一樣要改成自訂的樣式
                $('.new-task > .jqx-kanban-item-avatar').remove();
                $('.new-task > .jqx-kanban-item-footer').css('border-top-color', inputColor);
                $('.new-task')
                    .css('border-style', 'none')
                    .css('border-radius', '4px')
                    .css('margin-top', '8px')
                    .css('margin-bottom', '8px')
                    .css('background-color', inputColor)
                    .mouseup(function (e) {
                        $(e.target).closest('.jqx-kanban-item').css('box-shadow', '0 2px 4px 0 rgba(0, 0, 0, 0.1), 0 2px 5px 0 rgba(0, 0, 0, 0.089)');
                    })
                    .mousedown(function(e) {
                        $(e.target).closest('.jqx-kanban-item').css('box-shadow', '0 6px 25px 0 rgba(0, 0, 0, 0.25)');
                    })
                $('.new-task > .jqx-kanban-item-text')
                    .css('color', textColor[colorArray.indexOf(inputColor)])
                    .addClass('kanban-item-text')
                    .removeClass('jqx-kanban-item-text');
                $('.new-task > .jqx-kanban-item-color-status').remove();
                $('.new-task').removeClass('new-task');
                
            }
        }
    });

    // 以下是把jQWidget預設樣式改掉的部分
    $('.jqx-kanban-item-avatar').remove();
    $('.jqx-kanban-column-header').css('height', '36.652px');
    $('.jqx-kanban-item')
        .css('border-style', 'none')
        .css('border-radius', '4px')
        .css('margin-top', '8px')
        .css('margin-bottom', '8px')
        .mouseup(function (e) {
            $(e.target).closest('.jqx-kanban-item').css('box-shadow', '0 2px 4px 0 rgba(0, 0, 0, 0.1), 0 2px 5px 0 rgba(0, 0, 0, 0.089)');
        })
        .mousedown(function(e) {
            $(e.target).closest('.jqx-kanban-item').css('box-shadow', '0 8px 20px 5px rgba(0, 0, 0, 0.25)');
        });
    var kanbanItem = document.getElementsByClassName('jqx-kanban-item');
    var kanbanColor = document.getElementsByClassName('jqx-kanban-item-color-status');
    var text = document.getElementsByClassName('jqx-kanban-item-text');
    var kanbanBorder = document.getElementsByClassName('jqx-kanban-item-footer');
    var i = 0;
    for(i = 0 ; i<kanbanItem.length ; i++){
        bgColor = kanbanColor[i].style.backgroundColor
        kanbanItem[i].style.backgroundColor = bgColor;
        kanbanBorder[i].style.borderTopColor = bgColor;
        text[i].style.color = textColor[colorArray.indexOf(rgbToHex(bgColor))];
    }
    $('.jqx-kanban-item-text').addClass('kanban-item-text')
    .removeClass('jqx-kanban-item-text');
    $('.jqx-kanban-item-color-status').remove();
});

function getRandom(min,max){
    return Math.floor(Math.random()*(max-min+1))+min;
};

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
};

