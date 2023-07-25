
import React from "react";

const PreviousButton = props => (
    <button
        className="previous"
        onClick={props.onClick}
        disabled={props.counter + 1 === 1}
    >
        Previous
    </button>
);

export default PreviousButton;

