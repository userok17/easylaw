function snackbar(text, status) {
    // Get the snackbar DIV
    var x = $('#snackbar')
    
    x.text(text)

    // Add the "show" class to DIV
    x.addClass("show");
    x.addClass(status);

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.removeClass('show'); x.removeClass(status);}, 2000);
}
/*
 * Если пользователь кликнул на span.editable
 */
function spanClicked() {
    var editableText = $('<input type="text" class="editable" />');
    
    //записываем данные с data-value и с data-placeholder в input
    editableText.data('value', $(this).data('value'));
    editableText.data('placeholder', $(this).data('placeholder'));
    
    //Если data-value не пустая, то вставляем с data-value
    if($(this).data('value').trim() != ''){
        editableText.val($(this).data('value'));
    }
    //keypress и вводить данные c value в data-value
    editableText.keyup(function(){
        $(this).data('value', $(this).val());
    })
    $(this).replaceWith(editableText);
    editableText.focus();
    // setup the blur event for this new textarea
    editableText.blur(editableTextBlurred);
    // Нажатие на Enter
    editableText.keypress(function(e){
        if(e.keyCode == 13){
          editableText.blur();
        }
    });
}
/*
 * Если пользователь убрал с фокуса или нажал Enter
 */
function editableTextBlurred() {
    var viewableText = $('<span class="editable">');
    ////записываем данные с data-value и с data-placeholder в span +
    viewableText.data('value', $(this).data('value'));
    viewableText.data('placeholder', $(this).data('placeholder'));
    // Проверяем data-value, если пустая, то вставляем с data-placeholder
    // иначе Вставляем с data-value
    if($(this).data('value').trim() == ''){
        viewableText.text($(this).data('placeholder'));
    } else{
        viewableText.text($(this).data('value'));
    }
    
    $(this).replaceWith(viewableText);
    // setup the click event for this new div
    viewableText.click(spanClicked);
}

$(document).ready(function() {
    $('span.editable').click(spanClicked);
    
    // Получить файл
    $('#form-blank').submit(function(e){
      var foundFirstElementError = false;
      var offsetFirstElementError = 0;
        $('.editable').each(function(idx){
            if($(this).data('value') == ''){
              $(this).addClass('error');
              if(foundFirstElementError == false){
                    offsetFirstElementError = $(this).offset().top - 30;
                    foundFirstElementError = true;
              }
            
          }
        });
        if(foundFirstElementError){
          
          $('html, body').animate(
            {scrollTop: offsetFirstElementError},
            {
                complete: function(){
                    snackbar('Заполните все данные текущего документа', 'error');
                }
            }
          );
          e.preventDefault();
        }
        // Записываем данные документа в форму
        var content = $('#content-blank').html();
        $('#form-blank input[name="blank"]').val(content);
    });
    
    /*
     * Добавить или удалить в закладки
     */
    $('#bookmark-add').click(function(e){
        e.preventDefault();
        var self = $(this);
        $.ajax({
            type: 'GET',
            url: '/cabinet/bookmark_add/',
            data: {blank_id: blank_id},
            dataType: 'json',
            success: function(data)
            {
                if(data['status'] == 'success'){
                    self.html('<i class="fa fa-bookmark" aria-hidden="true"></i> ' + data['method']);
                } else{
                    snackbar(data['message'], 'error')
                }
                
            },
            error: function(msg)
            {
                snackbar('Что-то пошло не так!', 'error');
            }
        });
    });
    
    /*
     * Комментарии
     */
    // Авторазмер textarea
    $('#form-comment textarea').autogrow({vertical: true, horizontal: false});
    
    // Если есть данные то сделать кнопку активной
    $('#form-comment textarea').keypress(function(){
        if($(this).val().trim().length > 0){
            $(this).closest('#form-comment').find('button').prop('disabled', false);
        } else{
            $(this).closest('#form-comment').find('button').prop('disabled', true);
        }
    });
    $('#form-comment').submit(function(e){
        e.preventDefault();
        var $self = $(this);
        var str = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: window.location.pathname,
            data: str,
            dataType: 'json',
            success: function(data)
            {
                if(data['status'] == 'success'){
                    $self.find('textarea').val('');
                    $self.find('button').prop('disabled', true);
                    var new_item = $(data['body']).hide();
                    new_item.prependTo($('div.comments'));
                    new_item.fadeIn('slow');
                    var count = $('#comment-count');
                    count.text(data['count']);
                    
                    snackbar('Ваш комментарий успешно добавлен!', 'success')
                } else{
                    snackbar(data['message'], 'error')
                }
                
            },
            error: function(msg)
            {
                snackbar('Что-то пошло не так!', 'error');
            }
        });
    
        });
});