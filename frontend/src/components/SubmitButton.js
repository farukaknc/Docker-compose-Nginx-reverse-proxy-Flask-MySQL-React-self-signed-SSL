import React from "react";

const SubmitButton = props => (
    <button
        className="submit"
        onClick={props.onClick}
    >
        Submit
    </button>
);

export default SubmitButton;