import React from "react";

const NextButton = props => (
    <button
        className="next"
        onClick={props.onClick}
        disabled={props.counter + 1 === props.totalQuestion}
    >
        Next
    </button>
);

export default NextButton;

