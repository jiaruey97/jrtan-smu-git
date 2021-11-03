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
            { text: 'Prerequisite', value: 'Prerequisite' },
            { text: 'Start_Time', value: 'Start_Time' },
            { text: 'End_Time', value: 'End_Time' },
            { text: 'Sections', value: 'Sections' },
            { text: 'Class', value: 'Class' },
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
        enrolled_course: [],
        class_list: [],
        course_pending: [],
        enrollment_dates: [],
        mode: true,
        user: params.user,
        enrollment_period: true,
    },

    created() {
        this.check_enrollment_period()
        this.initialise_enrolled_course()
        this.initialise_course_to_enroll()
        this.initialise_pending_course()
        console.log(this.enrollment_dates)
    },
    computed: {

    },
    methods: {

        check_enrollment_period: function () {
            placehold_array_4 = Array()
            axios.get(`http://3.131.65.207:5944/spm/enrollment_date`)
                .then(function (response) {
                    date_array = response.data.data.enroll
                    for (let index = 0; index < date_array.length; index++) {
                        ending = date_array[index].Enrollment_End
                        starting = date_array[index].Enrollment_Start

                        now_time = Date.parse(today) - 28, 800, 000

                        if (now_time > Date.parse(starting) & now_time < Date.parse(ending)) {
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
                .catch(function (error) {
                    console.log(error)
                })

            this.enrollment_dates = placehold_array_4
        },

        initialise_enrolled_course: function () {
            placehold_array = Array()
            axios.get(`http://${addressUser}/user_database/`+this.user)
                .then(function (response) {
                    user = response.data.data.user[0]
                    courses = user.Course_Assigned
                    print(courses)
                    courses = JSON.parse(courses)
                    console.log(courses)
                    for (course of courses) {
                        id = course.course
                        console.log(id)
                        class_id = course.class
                        axios.get(`http://${addressCourse}/spm/course_retrieve/` + id)
                            .then(function (response) {
                                retreived_courses = response.data.data
                                placehold = {
                                    Course_ID: retreived_courses.Course_ID,
                                    Course_Name: retreived_courses.Course_Name,
                                    Duration: retreived_courses.Duration,
                                    Prerequisite: retreived_courses.Prerequisite,
                                    Start_Time: retreived_courses.Start_Time,
                                    End_Time: retreived_courses.End_Time,
                                    Class: class_id,
                                    Sections: retreived_courses.Sections
                                }
                                placehold_array.push(placehold)
                            })
                    }
                    console.log(placehold_array)

                })
                .catch(function (error) {
                    console.log(error)
                })

            this.enrolled_course = placehold_array
        },

        initialise_course_to_enroll: function () {
            placehold_array_2 = Array()
            axios.get(`http://${addressUser}/user_database/` + this.user)
                .then(function (response) {
                    user = response.data.data.user[0]
                    course_assigned = JSON.parse(user.Course_Assigned)
                    course_completed = JSON.parse(user.Course_Completed)
                    course_pending = JSON.parse(user.Course_Pending)
                    
                    course_assigned_array = Array()
                    course_complete_array = Array()
                    course_pending_array = Array()
                
                    for (let index = 0; index < course_assigned.length; index++) {
                        course_assigned_array.push(course_assigned[index].course)
                    }

                    for (let index = 0; index < course_completed.length; index++) {
                        course_complete_array.push(course_completed[index].course)
                    }

                    for (let index = 0; index < course_pending.length; index++) {
                        course_assigned_array.push(course_pending[index].course)
                    }


                    axios.get(`http://${addressCourse}/spm/course`)
                        .then(function (response) {
                            course_list = response.data.data.course
                            console.log(course_list)
                            for (let index = 0; index < course_list.length; index++) {
                                course = course_list[index]
                                pre = course.Prerequisite.split(",")
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
                                    if (course_assigned_array.find(element => element == course.Course_ID) == undefined) {
                                        if (course_complete_array.find(element => element == course.Course_ID) == undefined) {
                                            if (course_pending_array.find(element => element == course.Course_ID) == undefined) {
                                                placehold = {
                                                    Course_ID: course.Course_ID,
                                                    Course_Name: course.Course_Name,
                                                    Duration: course.Duration,
                                                    Prerequisite: course.Prerequisite,
                                                    Start_Time: course.Start_Time,
                                                    End_Time: course.End_Time,
                                                    Sections: course.Sections,
                                                    Course_Pending: course_pending
                                                }
                                                placehold_array_2.push(placehold)
                                            }
                                        }
                                    }
                                }
                            }
                        })
                        .catch(function (error) {
                            console.log(error)
                        })
                })
                .catch(function (error) {
                    console.log(error)
                })

            this.course_list = placehold_array_2
        },



        initialise_pending_course: function () {
            placehold_array_5 = Array()
            axios.get(`http://${addressUser}/user_database/` + this.user)
                .then(function (response) {
                    user = response.data.data.user[0]
                    course_pending = JSON.parse(user.Course_Pending)
                    console.log(course_pending)
                    for (let index = 0; index < course_pending.length; index++) {
                        id = course_pending[index]
                        axios.get(`http://${addressCourse}/spm/course_retrieve/` + id.course)
                            .then(function (response) {
                                console.log(response)
                                courses = response.data.data
                                placehold_5 = {
                                    Course_ID: courses.Course_ID,
                                    Course_Name: courses.Course_Name,
                                    Duration: courses.Duration,
                                    Prerequisite: courses.Prerequisite,
                                    Start_Time: courses.Start_Time,
                                    End_Time: courses.End_Time,
                                    Sections: courses.Sections,
                                    Class: id.class,
                                    Course_Pending: course_pending,
                                }
                                placehold_array_5.push(placehold_5)
                            })
                            .catch(function (error) {
                                console.log(error)
                            })
                    }
                })
                .catch(function (error) {
                    console.log(error)
                })

            this.course_pending = placehold_array_5
        },

        delete_enrollment: function (stuff) {
            course_pending_list = stuff.Course_Pending
            course_delete = stuff.Course_ID

            for (let index = 0; index < course_pending_list.length; index++) {
                pending_item = course_pending_list[index]
                if (pending_item.course == course_delete) {
                    course_pending_list.splice(index, 1)
                }
            }

            post_object_3 = {
                'Course_Pending': JSON.stringify(course_pending_list)
            }

            axios.post(`http://${addressUser}/user_database/` + this.user + `/update`, post_object_3)
                .then(function (response) {
                    alert("Update to User successful")
                })
                .catch(function (error) {
                    alert("Something when wrong with the Update")
                })
        },


        select_class: function (stuff) {
            course_id = stuff.Course_ID
            console.log(stuff.Course_ID)
            this.mode = false
            placehold_array_3 = Array()
            now_time = Date.parse(today) - 28, 800, 000

            axios.get(`http://${addressClass}/spm/search_class_course/` + course_id)
                .then(function (response) {
                    console.log(response)
                    class_list = response.data.data.class
                    for (let index = 0; index < class_list.length; index++) {
                        class_details = class_list[index]
                        console.log(class_details)
                        if (class_details.Size > class_details.Current_Size) {
                            if (Date.parse(class_details.Start_Time) > now_time) {
                                placehold = {
                                    Class_ID: class_details.Class_ID,
                                    Class_Name: class_details.Class_Name,
                                    Class_Details: class_details.Class_Details,
                                    Current_Size: class_details.Current_Size,
                                    Size: class_details.Size,
                                    Instructor: class_details.Instructor_ID,
                                    Start_Time: class_details.Start_Time,
                                    End_Time: class_details.End_Time,
                                    Sections: class_details.Sections,
                                    Students: class_details.Students,
                                    Course_ID: course_id,
                                    Course_Pending: stuff.Course_Pending
                                }
                                placehold_array_3.push(placehold)
                            }
                        }
                    }

                })
                .catch(function (error) {
                    console.log(error)
                })

            this.class_list = placehold_array_3
        },

        enroll_complete: function (stuff) {
            console.log(stuff)
            current_pending_course = stuff.Course_Pending

            storage_object = {
                course: stuff.Course_ID,
                class: stuff.Class_ID
            }
            current_pending_course.push(storage_object)

            post_object_2 = {
                'Course_Pending': JSON.stringify(current_pending_course)
            }

            axios.post(`http://${addressUser}/user_database/` + user.Username + `/update`, post_object_2)
            .then(function (response) {
                alert("Update to User successful")
            })
            .catch(function (error) {
                alert("Something when wrong with the Update")
            })

        },

        enter_class: function (course_item) {
            console.log(course_item)
            class_id = course_item.Class
            course_id = course_item.Course_ID
            course_name = course_item.Course_Name
            url_to_visit = "course_page_learner.html?class=" + class_id.toString() + "&course_id=" + course_id.toString() + "&course_name=" + course_name 
            window.open(url_to_visit, '_blank')
        }

    }
})

//Cleaning up messy json
function clean_json(json_str) {
    json_str = json_str.replace(/\\n/g, "\\n")
        .replace(/\\'/g, "\\'")
        .replace(/\\"/g, '\\"')
        .replace(/\\&/g, "\\&")
        .replace(/\\r/g, "\\r")
        .replace(/\\t/g, "\\t")
        .replace(/\\b/g, "\\b")
        .replace(/\\f/g, "\\f");
    // remove non-printable and other non-valid JSON chars
    json_str = json_str.replace(/[\u0000-\u0019]+/g, "");
    return json_str
}