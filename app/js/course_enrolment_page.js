const addressCourse = "3.131.65.207:5144"
const addressUser = "3.131.65.207:5744"
const addressClass = "3.131.65.207:5044"

const urlSearchParams = new URLSearchParams(window.location.search)
const params = Object.fromEntries(urlSearchParams.entries())

const today = new Date();

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

          headers_date: [
            {
                text: 'Enrollment ID',
                align: 'start',
                value: 'Enrollment_ID',
              },
              { text: 'Enrollment Start', value: 'Enrollment_Start' },
              { text: 'Enrollment_End', value: 'Enrollment_End' },

            ],
        
        course_list: [],
        enrolled_course:[],
        class_list:[],
        course_pending:[],
        enrollment_dates:[],
        mode: true,
        user: params.user,
        enrollment_period: true,
    },

    created(){    
        this.check_enrollment_period()
        this.initialise_enrolled_course()
        this.initialise_course_to_enroll()
        this.initialise_pending_course()
        console.log(this.enrollment_dates)
    }, 
    computed: {

    },
    methods: {

        check_enrollment_period: function(){
            placehold_array_4 = Array()
            axios.get(`http://3.131.65.207:5944/spm/enrollment_date`)
            .then(function (response) {
                date_array = response.data.data.enroll
                for (let index = 0; index < date_array.length; index++) {
                    ending = date_array[index].Enrollment_End
                    starting = date_array[index].Enrollment_Start
                    
                    now_time = Date.parse(today) - 28,800,000

                    if (now_time > Date.parse(starting) & now_time< Date.parse(ending)) {
                        this.enrollment_period = false
                        date_placeholder = {
                            Enrollment_ID: date_array[index].Enrollment_ID,
                            Enrollment_Start: starting,
                            Enrollment_End: ending,
                        }
                    }

                    placehold_array_4.push(date_placeholder)
                }                
            })
            .catch( function (error) {
                console.log(error)
            })

            this.enrollment_dates = placehold_array_4
        },




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
                course_pending = user.Course_Pending
                course_assigned = course_assigned.split(',')
                course_completed = course_completed.split(',')
                course_pending = course_pending.split(',')

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
                                    if (course_pending.find(element => element == course.Course_ID) == undefined) {
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

        
        
        initialise_pending_course: function(){
            placehold_array_5 = Array()
            axios.get(`http://${addressUser}/user_database/` + this.user)
            .then(function (response) {
                user = response.data.data.course[0]
                course_pending = user.Course_Pending
                course_pending = course_pending.split(',')
                console.log(course_pending)
                for (let index = 0; index < course_pending.length; index++) {
                    id = course_pending[index]
                    axios.get(`http://${addressCourse}/spm/course_retrieve/` + id)
                    .then(function (response) {
                        console.log(response)
                        courses = response.data.data    
                            placehold_5 = {
                                Course_ID:courses.Course_ID,
                                Course_Name:courses.Course_Name,
                                Duration:courses.Duration,
                                Prerequestic: courses.Prerequestic,
                                Start_Time: courses.Start_Time,
                                End_Time: courses.End_Time,
                                Sections: courses.Sections,
                                Course_Pending: course_pending,
                            }
                            placehold_array_5.push(placehold_5)
                    })
                    .catch( function (error) {
                            console.log(error)
                        })
                }
            })
            .catch( function (error) {
                    console.log(error)
            })
                
            this.course_pending = placehold_array_5
        },

        delete_enrollment: function(stuff){
            course_pending_list = stuff.Course_Pending
            course_delete = stuff.Course_ID
            
            index = course_pending_list.indexOf(course_delete.toString())

            console.log(index)
            if (index > -1) {
            course_pending_list.splice(index, 1)
            }

            post_object_3 = {
                'Course_Pending': course_pending_list.toString()
            }

            axios.post(`http://${addressUser}/user_database/` + user.Username + `/update`, post_object_3)
            .then(function (response) {
                alert("Update to User successful")
            })
            .catch( function (error) {
                alert("Something when wrong with the Update")
            })
        },


        select_class: function(stuff){
            course_id = stuff.Course_ID
            console.log(stuff.Course_ID)
            this.mode = false
            placehold_array_3 = Array()
            now_time = Date.parse(today) - 28,800,000

            axios.get(`http://${addressClass}/spm/search_class_course/` + course_id )
            .then(function (response) {
                console.log(response)
                class_list = response.data.data.course
                for (let index = 0; index < class_list.length; index++) {
                    class_details = class_list[index]
                    console.log(class_details)
                    if (class_details.Size > class_details.Current_Size) {
                        if(Date.parse(class_details.Start_Time)>now_time){
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
                }

            })
            .catch( function (error) {
                    console.log(error)
            })      
            
            this.class_list = placehold_array_3
        },

        enroll_complete: function(stuff){

            post_object_2 = {
                'Course_Pending': stuff.Course_ID
            }
            axios.post(`http://${addressUser}/user_database/` + user.Username + `/update`, post_object_2)
            .then(function (response) {
                alert("Update to User successful")
            })
            .catch( function (error) {
                alert("Something when wrong with the Update")
            })
             
        },

        enter_class: function(stuff){
            console.log(stuff)
            alert("redirect to url")
        }

    }
})
