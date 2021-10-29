const addressCourse = "3.131.65.207:5144"
const addressUser = "3.131.65.207:5744"

const address = fetch(`http://${addressUser}/user_database/Tommy`)
.then((response) => response.json())
.then((user) => {
  return user.data.course[0];
});

const printAddress = async () => {
    const a = await address;
    console.log(a)
};

const quiz_app = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        headers: [
            {
              text: 'Course ID',
              align: 'start',
              value: 'Course_ID',
            },
            { text: 'Course Name', value: 'Course_Name' },
            { text: 'Duration', value: 'Duration' },
            { text: 'Prerequestic', value: 'Prerequestic' },
            { text: 'Start_Time', value: 'Start_Time' },
            { text: 'End_Time', value: 'End_Time' },
            { text: 'Sections', value: 'Sections' },
            { text: 'Actions', value: 'actions' },
          ],
        
        course_list: [],
        enrolled_course:[],
        test:"",
    },

    created(){    
        this.initialise_course()
        
    }, 
    computed: {
        returnQuiz: function() {
            return this.questions
        }
    },
    methods: {
        initialise_course: function(){

            placehold_array = Array()
            
            console.log(printAddress().Actual_Name)

            
                axios.get(`http://${addressCourse}/spm/course`)
                .then(function (response) {
                    courses = response.data.data.course
                    console.log(courses)
                    for (let i = 0; i < courses.length; i++) {

                        placehold = {
                            Course_ID:courses[i].Course_ID,
                            Course_Name:courses[i].Course_Name,
                            Duration:courses[i].Duration,
                            Prerequestic: courses[i].Prerequestic,
                            Start_Time: courses[i].Start_Time,
                            End_Time: courses[i].End_Time,
                            Sections: courses[i].Sections
                        }
                        placehold_array.push(placehold)
                    }
        
                })
                .catch( function (error) {
                        console.log(error)
                    })
            
            
            

    
    
            this.course_list = placehold_array
        },





    }
})

async function initialise_user(){
    return await axios.get(`http://${addressUser}/user_database/Tommy`)
    .then(response => {
      this.response = response.data
      console.log(this.response)
      return this.response.data.course[0]
    })
}