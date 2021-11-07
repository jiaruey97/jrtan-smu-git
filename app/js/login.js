const courseAddress = '3.131.65.207:5144'
const materialAddress = '3.131.65.207:5344'
const classAddress='3.131.65.207:5044'
const userAddress='3.131.65.207:5744'
const instructAddress = "3.131.65.207:5244"

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

        axios.get(`http://${userAddress}/user_database/${this.Username}`)
          .then(function (response) {
            redirect = response.data.data.user[0]
            console.log(redirect)
            if (redirect.Current_Position == "Learner") {
              window.location.href = './course_enrolment_page.html?user=' + redirect.Username
            }
            if (redirect.Current_Position == "HR") {
              window.location.href = './HR_webpage.html'
            }
            if (redirect.Current_Position == "Instructor") {
              axios.get(`http://${instructAddress}/spm/instructor`)
              .then(function (response) {
                
                instruct = response.data.data.instructor
                console.log(instruct)
                for (let index = 0; index < instruct.length; index++) {
                  console.log(this.Username)
                  if (instruct[index].Username == redirect.Username) {
                    window.location.href = './course_page_trainer.html?instructor=' + instruct[index].Instructor_ID
                  }
                }

              })
              .catch(function (error) {
                console.log(error)
              })
            }
          })
          .catch(function (error) {
            console.log(error)
          })


      }
    },
    data: () => ({
      dialog: true,
      tab: 0,
      tabs: [
          {name:"Login", icon:"mdi-account"},
      ],
      valid: true,
      Username:"",

    })
  });


  
  