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
    },

    created(){    
        this.initialise_enrolled_course()
        this.initialise_course_to_enroll()
        
    }, 
    computed: {
        returnQuiz: function() {
            return this.questions
        }
    },
    methods: {
        initialise_enrolled_course: function(){
            placehold_array = Array()
            axios.get(`http://${addressUser}/user_database/Tommy`)
            .then(function (response) {
                user = response.data.data.course[0]
                course = user.Course_Assigned
                course = course.split(',')
                for (let index = 0; index < course.length; index++) {
                    id = index + 1
                    axios.get(`http://${addressCourse}/spm/course_retrieve/` + id)
                    .then(function (response) {
                        courses = response.data.data    
                            placehold = {
                                Course_ID:courses.Course_ID,
                                Course_Name:courses.Course_Name,
                                Duration:courses.Duration,
                                Prerequestic: courses.Prerequestic,
                                Start_Time: courses.Start_Time,
                                End_Time: courses.End_Time,
                                Sections: courses.Sections
                            }
                            placehold_array.push(placehold)
            
                    })
                    .catch( function (error) {
                            console.log(error)
                        })
                }
    
            })
            .catch( function (error) {
                    console.log(error)
                })
                
            this.enrolled_course = placehold_array
        },
asdsadsad
        initialise_course_to_enroll: function(){
            placehold_array_2 = Array()
            axios.get(`http://${addressUser}/user_database/Tommy`)
            .then(function (response) {
                user = response.data.data.course[0]
                course_assigned = user.Course_Assigned
                course_completed = user.Course_Completed
                course_assigned = course_assigned.split(',')
                course_completed = course_completed.split(',')

                axios.get(`http://${addressCourse}/spm/course`)
                .then(function (response) {
                    course_list = response.data.data.course
                    for (let index = 0; index < course_list.length; index++) {
                        course = course_list[index]
                        pre = course.Prerequestic.split(",")
                        fufilled_condition = 0

                        for (let index_1 = 0; index_1 < pre.length; index_1++) {
                            if (pre[index_1] == "") {
                                fufilled_condition += 1
                        }
                            if (course_completed.find(element => element == pre[index_1]) != undefined) {
                                fufilled_condition += 1
                                can_be_taken = false
                            }
                        }

                        if (pre.length == fufilled_condition) {
                            if (course_assigned.find(element => element == course.Course_ID) == undefined) {
                                if (course_completed.find(element => element == course.Course_ID) == undefined) {
                                    placehold = {
                                        Course_ID:course.Course_ID,
                                        Course_Name:course.Course_Name,
                                        Duration:course.Duration,
                                        Prerequestic: course.Prerequestic,
                                        Start_Time: course.Start_Time,
                                        End_Time: course.End_Time,
                                        Sections: course.Sections
                                    }
                                    placehold_array_2.push(placehold)
                                }
                            }
                        }
                    }
                })
                .catch( function (error) {
                        console.log(error)
                })        
            })
            .catch( function (error) {
                    console.log(error)
            })
                
            this.course_list = placehold_array_2
        },





    }
})
