tinymce.init({
  selector:'textarea#id_description',
  menubar: false,
  language: 'ru',
  language_url: '/static/js/tiny_mce/langs/ru.js',
  plugins: [
    'autoresize preview code',
  ],
  toolbar1: 'undo redo | bold italic | alignleft aligncenter alignright alignjustify | code | preview | formatselect',
  width: '90%',
  height: '300',
  theme_advanced_resizing: 'true',
  content_css: ['https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css', '/static/css/tiny_mce/tag_editable.css']
});

tinymce.init({
  selector:'textarea#id_text',
  menubar: false,
  language: 'ru',
  language_url: '/static/js/tiny_mce/langs/ru.js',
  plugins: [
    'autoresize tag_editable preview code',
  ],
  toolbar1: 'undo redo | bold italic | alignleft aligncenter alignright alignjustify | code | preview | formatselect',
  toolbar2: 'tag_editable',
  width: '90%',
  height: '300',
  theme_advanced_resizing: 'true',
  content_css: ['https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css', '/static/css/tiny_mce/tag_editable.css']
});

