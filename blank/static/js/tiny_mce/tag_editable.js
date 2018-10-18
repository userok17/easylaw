tinyMCE.PluginManager.add('tag_editable', function(editor, url) {
  editor.addButton('tag_editable', {
    text: "Тег редактирования бланка",
    icon: false,
    onclick: function() {
      var content = editor.selection.getContent();
      if(content.length == 0){
        var $ = django.jQuery;
        var span = $(editor.selection.getNode());
        
        if(span.prop('tagName') == 'SPAN' && span.prop('class') == 'editable'){
          text = span.text();
          span.contents().unwrap();
          editor.windowManager.alert('Фрагмент "' + text + '" удален из режима редактирования');
        }
        return;
      }
      else{
        editor.focus();
        editor.selection.setContent('<span class="editable" data-placeholder="' + content + '" data-value="">' + content + '</span>');
        editor.windowManager.alert('"' +  content + '" в режиме радактирования');
      }
      
    }
  });
});