const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const alertBox = document.getElementById('alert-box')

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}


Dropzone.autoDiscover = false
Dropzone.prototype.defaultOptions.dictDefaultMessage = 'Перетащите ваш файл сюда'
Dropzone.prototype.defaultOptions.dictFileTooBig = 'Файл превышает размер 3 MB'
Dropzone.prototype.defaultOptions.dictMaxFilesExceeded = 'Не более 3х файлов'
const myDropzone = new Dropzone('#my-dropzone', {
    url: '/reports/upload/',
    init: function(){
        this.on('sending', function(file, xhr, formData){
            console.log('sending')
            formData.append('csrfmiddlewaretoken', csrf)

        })
        this.on('success', function(file, response){
            const ex = response.ex
            if(ex) {
                    handleAlerts('danger', 'Файл с таким именем уже был обработан!')
            } else {
                    handleAlerts('success', 'Файл обработан!')
            }
        })
    },
    maxFiles: 3,
    maxFilesize: 3,
    acceptedFiles: '.csv'
})

