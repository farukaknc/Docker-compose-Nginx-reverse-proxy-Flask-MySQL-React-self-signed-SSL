import React from "react";
import { Formik } from "formik";

const loginPage = props => {
    <>
        <Formik>
            {({
                errors,
                touched,
                handleBlur,
            }) => (
                <div className="login">
                    <div className="form">
                        <form noValidate>
                            <span>Login</span>
                            <label>Email</label>
                            <input
                                type="email"
                                name="email"
                                onChange={(event) => setUserEmail(event.target.value)}
                                onBlur={handleBlur}
                                placeholder="Enter email"
                                className="form-control inp_text"
                                id="email"
                            />
                            <p className="error">
                                {errors.email && touched.email && errors.email}
                            </p>
                            <label>Name</label>
                            <input
                                type="text"
                                name="password"
                                onChange={(event) => setUserName(event.target.value)}
                                onBlur={handleBlur}
                                placeholder="Name"
                                className="form-control"
                            />
                            <p className="error">
                                {errors.password && touched.password && errors.password}
                            </p>
                            <button type="submit" onClick={() => setLoginPage(true)}>Next</button>
                        </form>
                    </div>
                </div>
            )}
        </Formik>
    </>
}

export default loginPage;