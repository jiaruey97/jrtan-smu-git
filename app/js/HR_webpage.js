<<<<<<< HEAD
const addressCourse = "3.131.65.207:5144"
const addressUser = "3.131.65.207:5744"
const addressClass = "3.131.65.207:5044"
const addressInstructor = "3.131.65.207:5244"
const trackerAddress = '3.131.65.207:5644'

const urlSearchParams = new URLSearchParams(window.location.search)
const params = Object.fromEntries(urlSearchParams.entries())

const today = new Date();

const quiz_app = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {

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

          headers_instructor: [
            {
                text: 'Instructor_ID',
                align: 'start',
                value: 'Instructor_ID',
              },
              { text: 'Actual Name', value: 'Actual_Name' },
              { text: 'Username', value: 'Username' },
              { text: 'Actions', value: 'actions' },

            ],
            
            headers_enrollment:[
                {
                    text: 'User',
                    align: 'start',
                    value: 'Username',
                  },
                  { text: 'Course Pending', value: 'Course_ID' },
                  { text: 'Class', value: 'Class_ID' },
                  { text: 'Actions', value: 'actions' },
            ],
        
        class_details:[],
        instructor_list:[],
        enrollment_list:[],
        class_display: true,
        instructor_display:false,

    },

    created(){    
        this.initalise_all_class()
        this.initialise_enrollment()
    }, 
    computed: {

    },
    methods: {
        
        initalise_all_class: function(){
            placehold_array_4 = Array()
            axios.get(`http://${addressClass}/spm/class`)
            .then(function (response) {
                
                class_array = response.data.data.class
                console.log(class_array)
                for (let index = 0; index < class_array.length; index++) {
                    class_details = class_array[index]
                    date_placeholder = {
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
                        Course_ID: class_details.Course_ID,
                    }
                    placehold_array_4.push(date_placeholder)
                }                
            })
            .catch( function (error) {
                console.log(error)
            })

            this.class_details = placehold_array_4
        },

        assign_instructor: function(stuff){
            this.instructor_display = true
            this.class_display = false
            console.log(stuff)
            placehold_array = Array()
            axios.get(`http://${addressInstructor}/spm/instructor`)
            .then(function (response) {
                
                instructor_array = response.data.data.instructor
                console.log(instructor_array)
                for (let index = 0; index < instructor_array.length; index++) {
                    instructor_details = instructor_array[index]
                    instructor_placeholder = {
                        Instructor_ID:instructor_details.Instructor_ID,
                        Actual_Name:instructor_details.Actual_Name,
                        Username:instructor_details.Username,
                        Class_ID:stuff.Class_ID
                    }
                    placehold_array.push(instructor_placeholder)
                }                
            })
            .catch( function (error) {
                console.log(error)
            })

            this.instructor_list = placehold_array
        },

        choose_this_instructor: function(stuff){
            this.instructor_display = true
            this.class_display = false
            console.log(stuff)
            placehold_array = Array()

            post_object = {
                Instructor_ID:stuff.Instructor_ID
            }

            axios.post(`http://${addressClass}/class/` + stuff.Class_ID + `/update`,post_object)
            .then(function (response) {
                alert("Update Successful")         
            })
            .catch( function (error) {
                console.log(error)
            })

        },

        initialise_enrollment: function(){
            placehold_array2 = Array()
            axios.get(`http://${addressUser}/spm/user_database`)
            .then(function (response) {
                alert("hello")
                user_list = response.data.data.user
                console.log(user_list)
                for (let index = 0; index < user_list.length; index++) {
                    user = user_list[index]
                    console.log(user)
                    if (user.Course_Pending != "" & user.Course_Pending != "[]" ) {
                        course_list = JSON.parse(user.Course_Pending)
                        for (let i2 = 0; i2 < course_list.length; i2++) {
                            course_details = course_list[i2]

                            axios.get(`http://${addressClass}/spm/class_id/` + course_details.class)
                            .then(function (response) {
                                class_details = response.data.data.class[0]
                                back_array = course_list.slice(0, i2)
                                front_array = course_list.slice(i2+1)
                                remaing_array = front_array.concat(back_array)
                                console.log(remaing_array)

                                //Check if course asssigned is empty, if empty, initialize empty array
                                if (user.Course_Assigned == ""){
                                    user.Course_Assigned = []
                                } 

                                course_placeholder = {
                                    Username:user.Username,
                                    Course_Enrolled:user.Course_Assigned,
                                    Course_ID:course_details.course,
                                    Class_ID:course_details.class,
                                    Course_Remaining: remaing_array,
                                    Class_Current_Size: class_details.Current_Size,
                                    Class_Students: class_details.Students 
                                }
                                placehold_array2.push(course_placeholder)        
                            })
                            .catch( function (error) {
                                console.log(error)
                            })
                        }
                    }
                }         
            })
            .catch( function (error) {
                console.log(error)
            })
            this.enrollment_list = placehold_array2
        },


        student_acceptance: function(stuff){
            console.log(stuff)

            //Check if it's a valid json
            if(typeof(stuff.Course_Enrolled) != 'object'){
                //parse it
                course_assigned_array = JSON.parse(stuff.Course_Enrolled)
            } else {
                course_assigned_array = stuff.Course_Enrolled
            }
            course_assigned_array.push({course:stuff.Course_ID, class:stuff.Class_ID})

        
            post_object = {
                Course_Pending:JSON.stringify(stuff.Course_Remaining),
                Course_Assigned:JSON.stringify(course_assigned_array)
            }
            if (stuff.Class_Students == "") {
                student_array = [stuff.Username]
            }
            else{
                student_array = JSON.parse(stuff.Class_Students)
                student_array.push(stuff.Username) 
            }


            post_object2 = {
                Current_Size: JSON.stringify(stuff.Class_Current_Size + 1),
                Students:JSON.stringify(student_array)
            }
            
            console.log(post_object2)
            console.log(post_object)

            axios.post(`http://${addressClass}/class/` + stuff.Class_ID + "/update", post_object2)
            .then(function (response) {
                alert("Class Update Successful")         
            })
            .catch( function (error) {
                console.log(error)
            })
        
            axios.post(`http://${addressUser}/user_database/` + stuff.Username + "/update", post_object)
            .then(function (response) {
                alert("User Update Successful")         
            })
            .catch( function (error) {
                console.log(error)
            })

            axios.get(`http://${trackerAddress}/create_tracker/${stuff.Username}/${stuff.Course_ID}/${stuff.Class_ID}`)
            .then(function (response) {
                alert("Tracking update successful")         
            })
            .catch( function (error) {
                console.log(error)
            })
            
        },

        student_rejection: function (stuff) {
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
        
            axios.post(`http://${addressUser}/user_database/` + stuff.Username + `/update`, post_object_3)
                .then(function (response) {
                    alert("Update to User successful")
                })
                .catch(function (error) {
                    alert("Something when wrong with the Update")
                })
        },

    }
})



function tryParseJSONObject (jsonString){
    try {
        var o = JSON.parse(jsonString);
        if (o && typeof o === "object") {
            return o;
        }
    }
    catch (e) { }

    return false;
=======
const addressCourse = "3.131.65.207:5144"
const addressUser = "3.131.65.207:5744"
const addressClass = "3.131.65.207:5044"
const addressInstructor = "3.131.65.207:5244"
const trackerAddress = '3.131.65.207:5644'

const urlSearchParams = new URLSearchParams(window.location.search)
const params = Object.fromEntries(urlSearchParams.entries())

const today = new Date();

const quiz_app = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {

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

          headers_instructor: [
            {
                text: 'Instructor_ID',
                align: 'start',
                value: 'Instructor_ID',
              },
              { text: 'Actual Name', value: 'Actual_Name' },
              { text: 'Username', value: 'Username' },
              { text: 'Actions', value: 'actions' },

            ],
            
            headers_enrollment:[
                {
                    text: 'User',
                    align: 'start',
                    value: 'Username',
                  },
                  { text: 'Course Pending', value: 'Course_ID' },
                  { text: 'Class', value: 'Class_ID' },
                  { text: 'Actions', value: 'actions' },
            ],
        
        class_details:[],
        instructor_list:[],
        enrollment_list:[],
        class_display: true,
        instructor_display:false,

    },

    created(){    
        this.initalise_all_class()
        this.initialise_enrollment()
    }, 
    computed: {

    },
    methods: {
        
        initalise_all_class: function(){
            placehold_array_4 = Array()
            axios.get(`http://${addressClass}/spm/class`)
            .then(function (response) {
                
                class_array = response.data.data.class
                console.log(class_array)
                for (let index = 0; index < class_array.length; index++) {
                    class_details = class_array[index]
                    date_placeholder = {
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
                        Course_ID: class_details.Course_ID,
                    }
                    placehold_array_4.push(date_placeholder)
                }                
            })
            .catch( function (error) {
                console.log(error)
            })

            this.class_details = placehold_array_4
        },

        assign_instructor: function(stuff){
            this.instructor_display = true
            this.class_display = false
            console.log(stuff)
            placehold_array = Array()
            axios.get(`http://${addressInstructor}/spm/instructor`)
            .then(function (response) {
                
                instructor_array = response.data.data.instructor
                console.log(instructor_array)
                for (let index = 0; index < instructor_array.length; index++) {
                    instructor_details = instructor_array[index]
                    instructor_placeholder = {
                        Instructor_ID:instructor_details.Instructor_ID,
                        Actual_Name:instructor_details.Actual_Name,
                        Username:instructor_details.Username,
                        Class_ID:stuff.Class_ID
                    }
                    placehold_array.push(instructor_placeholder)
                }                
            })
            .catch( function (error) {
                console.log(error)
            })

            this.instructor_list = placehold_array
        },

        choose_this_instructor: function(stuff){
            this.instructor_display = true
            this.class_display = false
            console.log(stuff)
            placehold_array = Array()

            post_object = {
                Instructor_ID:stuff.Instructor_ID
            }

            axios.post(`http://${addressClass}/class/` + stuff.Class_ID + `/update`,post_object)
            .then(function (response) {
                alert("Update Successful")         
            })
            .catch( function (error) {
                console.log(error)
            })

        },

        initialise_enrollment: function(){
            placehold_array2 = Array()
            axios.get(`http://${addressUser}/spm/user_database`)
            .then(function (response) {
                alert("hello")
                user_list = response.data.data.user
                console.log(user_list)
                for (let index = 0; index < user_list.length; index++) {
                    user = user_list[index]
                    console.log(user)
                    if (user.Course_Pending != "" & user.Course_Pending != "[]" ) {
                        course_list = JSON.parse(user.Course_Pending)
                        for (let i2 = 0; i2 < course_list.length; i2++) {
                            course_details = course_list[i2]

                            axios.get(`http://${addressClass}/spm/class_id/` + course_details.class)
                            .then(function (response) {
                                class_details = response.data.data.class[0]
                                back_array = course_list.slice(0, i2)
                                front_array = course_list.slice(i2+1)
                                remaing_array = front_array.concat(back_array)
                                console.log(remaing_array)

                                //Check if course asssigned is empty, if empty, initialize empty array
                                if (user.Course_Assigned == ""){
                                    user.Course_Assigned = []
                                } 

                                course_placeholder = {
                                    Username:user.Username,
                                    Course_Enrolled:user.Course_Assigned,
                                    Course_ID:course_details.course,
                                    Class_ID:course_details.class,
                                    Course_Remaining: remaing_array,
                                    Class_Current_Size: class_details.Current_Size,
                                    Class_Students: class_details.Students 
                                }
                                placehold_array2.push(course_placeholder)        
                            })
                            .catch( function (error) {
                                console.log(error)
                            })
                        }
                    }
                }         
            })
            .catch( function (error) {
                console.log(error)
            })
            this.enrollment_list = placehold_array2
        },


        student_acceptance: function(stuff){
            console.log(stuff)

            //Check if it's a valid json
            if(typeof(stuff.Course_Enrolled) != 'object'){
                //parse it
                course_assigned_array = JSON.parse(stuff.Course_Enrolled)
            } else {
                course_assigned_array = stuff.Course_Enrolled
            }
            course_assigned_array.push({course:stuff.Course_ID, class:stuff.Class_ID})

        
            post_object = {
                Course_Pending:JSON.stringify(stuff.Course_Remaining),
                Course_Assigned:JSON.stringify(course_assigned_array)
            }
            if (stuff.Class_Students == "") {
                student_array = [stuff.Username]
            }
            else{
                student_array = JSON.parse(stuff.Class_Students)
                student_array.push(stuff.Username) 
            }


            post_object2 = {
                Current_Size: JSON.stringify(stuff.Class_Current_Size + 1),
                Students:JSON.stringify(student_array)
            }
            
            console.log(post_object2)
            console.log(post_object)

            axios.post(`http://${addressClass}/class/` + stuff.Class_ID + "/update", post_object2)
            .then(function (response) {
                alert("Class Update Successful")         
            })
            .catch( function (error) {
                console.log(error)
            })
        
            axios.post(`http://${addressUser}/user_database/` + stuff.Username + "/update", post_object)
            .then(function (response) {
                alert("User Update Successful")         
            })
            .catch( function (error) {
                console.log(error)
            })

            axios.get(`http://${trackerAddress}/create_tracker/${stuff.Username}/${stuff.Course_ID}/${stuff.Class_ID}`)
            .then(function (response) {
                alert("Tracking update successful")         
            })
            .catch( function (error) {
                console.log(error)
            })
            
        },

        student_rejection: function (stuff) {
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
        
            axios.post(`http://${addressUser}/user_database/` + stuff.Username + `/update`, post_object_3)
                .then(function (response) {
                    alert("Update to User successful")
                })
                .catch(function (error) {
                    alert("Something when wrong with the Update")
                })
        },

    }
})



function tryParseJSONObject (jsonString){
    try {
        var o = JSON.parse(jsonString);
        if (o && typeof o === "object") {
            return o;
        }
    }
    catch (e) { }

    return false;
>>>>>>> 7c579483398a335ebf3b517b2d3cb1cd662dd9cd
};