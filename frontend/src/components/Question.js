import React from "react";

const Question = props => (
    <h2 className="question">{props.questions[props.counter].question}</h2>
);

export default Question;