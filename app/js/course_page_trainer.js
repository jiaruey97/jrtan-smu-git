const vueApp = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data () {
      return {
        selectedFile: null
      }

    },
    methods: {
      onFileSelected(event){
        console.log(event)
        this.selectedFile = event.target.files[0]
      },
      onUpload(){
        const fd = new FormData();
        fd.append('material', this.selectedFile, this.selectedFile.name)
        axios.post('Schema_Generation.sql', fd)
        .then(res => {
          console.log(res)
        })

      }

      },
      

  })