
var resizeTimeout;
var ckeditorXSToolbar = Array(
    { name: 'clipboard', groups: [ 'clipboard', 'undo' ], items: [ 'Cut', 'Copy', 'Paste','-', 'Undo', 'Redo' ] },
    { name: 'document', groups: [ 'mode' ], items: [ 'Source'] },
    { name: 'tools', items: [ 'Maximize'] },
    { name: 'styles', items: [ 'Format', 'Font', 'FontSize'] ,class:'hidden-xs'},
    { name: 'basicstyles', groups: [ 'basicstyles'], items: [ 'TextColor','Bold', 'Italic'] }

);

var ckeditorSMToolbar = [
    { name: 'styles', items: [ 'Styles', 'Format', 'Font', 'FontSize'] ,class:'hidden-xs'},
    { name: 'clipboard', groups: [ 'clipboard', 'undo' ], items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ] },
    { name: 'editing', groups: [ 'find', 'selection' ], items: [ 'Find', 'Replace', '-', 'SelectAll' ] },
    { name: 'document', groups: [ 'mode', 'document', 'doctools' ], items: [ 'Source', '-', 'Save', 'NewPage', 'Preview', 'Print'] },

    { name: 'forms', items: [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField' ] },
    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ], items: [ 'TextColor','Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat' ] },
    { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ], items: [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl', 'Language' ] },
    { name: 'tools', items: [ 'Maximize', 'ShowBlocks' ] }
];
var ckeditorMDToolbar = [
    { name: 'styles', items: [ 'Styles', 'Format', 'Font', 'FontSize'] ,class:'hidden-xs'},
    { name: 'clipboard', groups: [ 'clipboard', 'undo' ], items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ] },
    { name: 'editing', groups: [ 'find', 'selection', 'spellchecker' ], items: [ 'Find', 'Replace', '-', 'SelectAll', '-', 'Scayt' ] },
    { name: 'document', groups: [ 'mode', 'document', 'doctools' ], items: [ 'Source', '-', 'Save', 'NewPage', 'Preview', 'Print'] },

    { name: 'forms', items: [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField' ] },
    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ], items: [ 'TextColor','Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat' ] },
    { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ], items: [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl', 'Language' ] },
    { name: 'links', items: [ 'Link', 'Unlink', 'Anchor' ] },
    { name: 'insert', items: [ 'Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe' ] },

    { name: 'tools', items: [ 'Maximize', 'ShowBlocks' ] },
    { name: 'others', items: [ '-' ] },
    { name: 'about', items: [ 'About' ] }
];

function setupCKEdit(selector){
    if (typeof(o.snippets) == 'object'){
        var template = {
            imagesPath:url_img ,
            templates: o.snippets
        };
        CKEDITOR.addTemplates('myTemplate', template);
    }   
    resizeCKEdit();

    $('.ckeditor',selector).not('.hasCKEDITOR').each(function(index,element){
        $(this).addClass('hasCKEDITOR');
        var ckConfig = {
            templates_replaceContent:false,
            scayt_slang:'en_GB',
            scayt_autoStartup:scayt_autoStartup,
            toolbarCanCollapse:true,
            extraPlugins:'templates,colorbutton',
            toolbar:getCKtoolbar(),
            toolbarStartupExpanded:getCKToolbarStartup()
        };
        // inject the snippets after the toolbar[].name = 'document'
        if (typeof(o.snippets) == 'object'){
            ckConfig.templates = 'myTemplate';
            for(var i = 0 ; i < ckConfig.toolbar.length ; i++){
                if (ckConfig.toolbar[i].name == 'document'){
                    // iterate throught each document element to make sure template is not already there.
                    var hasTemplate = false;
                    for ( var j = 0 ; j < ckConfig.toolbar[i].items.length; j++){
                        if (ckConfig.toolbar[i].items[j] == 'Templates'){
                            hasTemplate = true;
                        }
                    }
                    if (hasTemplate == false){
                        ckConfig.toolbar[i].items.push('-'); // add to documents group.
                        ckConfig.toolbar[i].items.push('Templates');
                    }

                }
            }           
        }
        $(this).ckeditor(ckConfig);
        var editor = CKEDITOR.instances[this.id];
        if(typeof(editor) == 'object'){
            editor.on('blur',function(event){
                if (event.editor.checkDirty()){
                    var ta = $('#'+event.editor.name); // ta = textarea
                    if ( (typeof(ta) == 'object')
                        && (typeof(ta[0]) == 'object')
                        && ( $(ta[0]).hasClass('noajax') == false )
                        && ( $(ta[0]).data('id')) 
                        && ( ta[0].name)) {
                        var data = {
                            field_name:ta[0].name,
                            field_value:event.editor.getData(),
                            id:$(ta[0]).data('id')
                            };
                        data[ta[0].name]=event.editor.getData();
                        ajax_post(url_ajax + 'update_field', data);
                        event.editor.resetDirty();
                    }
                }
            });
        }
    });
}
function getCKtoolbar(){
    // returns the CK editor toolbar array based on window width
    var dw = $(document).width();
    if (dw < 768){
        return ckeditorXSToolbar;
    } else if(dw < 991){
        return ckeditorSMToolbar;
    }
    else {
        return ckeditorMDToolbar;
    }
}

function getCKToolbarStartup(){
    // returns the toolbarStartupExpanded parameter, based on window width
    var dw = $(document).width();
    if (dw < 768){
        return false;
    } else if(dw < 991){
        return true;
    }
    else {
        return true;
    }
    return true;
}
function resizeCKEdit(){
    // when there is a document resize, update the toolbar buttons.
    if ($('body').data('resize_enabled') == undefined){
        $('body').data('resize_enabled',true);
        $(window).resize(function(event){
            // only do the reize 100msec after the resizing finishes.
            window.clearTimeout(resizeTimeout);
            resizeTimeout = window.setTimeout(function(){

            // iterate through all CKEDITOR instances, and update their toolbars.
                var ckConfig = {
                    templates_replaceContent:false,
                    scayt_slang:'en_GB',
                    scayt_autoStartup:scayt_autoStartup,
                    toolbarCanCollapse:true,
                    extraPlugins:'templates,colorbutton',
                    toolbar:getCKtoolbar(),
                    toolbarStartupExpanded:getCKToolbarStartup()
                };
                if (CKEDITOR.editor.length){
                    // need to get all instances before deleting them,
                    var instances = Array();
                    var i = 0;
                    for (var instance in CKEDITOR.instances) {
                        instances[i] = instance;
                        i++;
                    }
                    for (i = 0 ; i < instances.length ; i ++){
                        CKEDITOR.instances[instances[i]].destroy();
                        $('#'+instances[i]).removeClass('hasCKEDITOR');
                        setupCKEdit($('#'+instances[i]).parent());
                    }
                }
            },200);

        });
    }
}
// ********* ck editor section ends **************