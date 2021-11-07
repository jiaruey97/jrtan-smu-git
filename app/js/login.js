const courseAddress = '3.131.65.207:5144'
const materialAddress = '3.131.65.207:5344'
const classAddress='3.131.65.207:5044'
const userAddress='3.131.65.207:5744'

const urlSearchParams = new URLSearchParams(window.location.search)
const params = Object.fromEntries(urlSearchParams.entries())

new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    computed: {
      usernameMatch() {
        return () => this.Username === this.verify || "username must match";
      }
    },
    data: {
      Username: '',
      course_id:params.course_id,
      // username = '',
      // Actual_Name: params.Actual_Name,
      // Course_Assigned: params.Course_Assigned,
      // Course_Completed: params.Course_Completed,
      // Course_Pending: params.Course_Completed,
      // Current_Position: params.Current_Position,
      // Department: params.Department,
      // chosen_course_name: params.course_name,
    },
    created() {
      // axios.get(`http://${materialAddress}/spm/materials/${this.course_id}`)
      axios.get(`http://${userAddress}/spm/user_database/${this.Username}`)
          .then(function (response) {
            return_response = response.data.data
            // console.log(course_id)
            console.log(Username)
  
            vueApp.validate()
          })
          .catch(function (error) {
            console.log(error)
          })
  
    },
    methods: {
      validate() {
        if (this.$refs.loginForm.validate()) {
          // submit form to server/API here...
        }
      },
      reset() {
        this.$refs.form.reset();
      },
      resetValidation() {
        this.$refs.form.resetValidation();
      },
      redirect() {
        // this.$router.push({name: ''})
        if("[user_database.Current_Position]" == "Instructor"){
          window.location = "instructor_assign.html";
          }
        else if ("[user_database.Current_Position]" == "HR"){
          window.location = "HR_webpage.html";
          }
        else{
          window.location = "course_enrolment_page.html?user=Tommy";
          }
      }
    },
    data: () => ({
      dialog: true,
      tab: 0,
      tabs: [
          {name:"Login", icon:"mdi-account"},
          
      ],
      valid: true,
      
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      verify: "",
      loginPassword: "",
      loginEmail: "",
      loginEmailRules: [
        v => !!v || "Required",
        // v => /.+@.+\..+/.test(v) || "E-mail must be valid"
      ],
      emailRules: [
        v => !!v || "Required",
        // v => /.+@.+\..+/.test(v) || "E-mail must be valid"
      ],
  
      show1: false,
      rules: {
        required: value => !!value || "Required.",
        // min: v => (v && v.length >= 8) || "Min 8 characters"
      }
    })
  });


  
  