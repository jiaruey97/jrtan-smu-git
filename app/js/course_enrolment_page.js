const addressCourse = "3.131.65.207:5144"
const addressUser = "3.131.65.207:5744"
const addressClass = "3.131.65.207:5044"


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

          headers_class: [
            {
              text: 'Class ID',
              align: 'start',
              value: 'Class_ID',
            },
            { text: 'Class Name', value: 'Class_Name' },
            { text: 'Class Details', value: 'Class_Details' },
            { text: 'Size', value: 'Size' },
            { text: 'Current_Size', value: 'Current_Size' },
            { text: 'Instructor', value: 'Instructor' },
            { text: 'Start_Time', value: 'Start_Time' },
            { text: 'End_Time', value: 'End_Time' },
            { text: 'Students', value: 'Students' },
            { text: 'Actions', value: 'actions' },
          ],
        
        course_list: [],
        enrolled_course:[],
        class_list:[],
        mode: true,
        user: "Tommy",
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
                    id = course[index]
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

        initialise_course_to_enroll: function(){
            placehold_array_2 = Array()
            axios.get(`http://${addressUser}/user_database/` + this.user)
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

        select_class: function(stuff){
            course_id = stuff.Course_ID
            console.log(stuff.Course_ID)
            this.mode = false
            placehold_array_3 = Array()

            axios.get(`http://${addressClass}/spm/search_class_course/` + course_id )
            .then(function (response) {
                console.log(response)
                class_list = response.data.data.course
                for (let index = 0; index < class_list.length; index++) {
                    class_details = class_list[index]
                    console.log(class_details)
                    if (class_details.Size > class_details.Current_Size) {
                        placehold = {
                            Class_ID:class_details.Class_ID,
                            Class_Name:class_details.Class_Name,
                            Class_Details:class_details.Class_Details,
                            Current_Size:class_details.Current_Size,
                            Size: class_details.Size,
                            Instructor: class_details.Instructor_ID,
                            Start_Time: class_details.Start_Time,
                            End_Time: class_details.End_Time,
                            Sections: class_details.Sections,
                            Students: class_details.Students,
                            Course_ID: course_id,
                        }
                        placehold_array_3.push(placehold)
                    }
                }

            })
            .catch( function (error) {
                    console.log(error)
            })      
            
            this.class_list = placehold_array_3
        },

        enroll_complete: function(stuff){
            class_id = stuff.Class_ID
            new_size = stuff.Current_Size + 1
            new_student = stuff.Students + "," + this.user


            post_object = {
                'Current_Size': new_size,
                'Students': new_student,      
            }

            axios.post(`http://${addressClass}/class/` + class_id + `/update`, post_object)
            .then(function (response) {
                console.log(response)
                alert("Update to Class successful")
            })
            .catch( function (error) {
                console.log(error)
                alert("Something when wrong with the Update")
            }) 
             
            axios.get(`http://${addressUser}/user_database/` + this.user)
            .then(function (response) {
                user = response.data.data.course[0]
                course_assigned = user.Course_Assigned
                course_new = course_assigned + "," + course_id
                console.log(course_new)
                console.log(class_id)
                console.log(this.user)
                post_object_2 = {
                    'Course_Assigned': course_new
                }
                axios.post(`http://${addressUser}/user_database/` + user.Username + `/update`, post_object_2)
                .then(function (response) {
                    alert("Update to User successful")
                })
                .catch( function (error) {
                    alert("Something when wrong with the Update")
                })
                
            })
            .catch( function (error) {
                console.log(error)
            })  




        }




    }
})
