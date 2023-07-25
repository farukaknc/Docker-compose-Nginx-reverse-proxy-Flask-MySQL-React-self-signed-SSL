import React from "react";

const QuestionCount = props => (
    <header>
        <div className="question-count">
            <h2>Question</h2>
            <div className="question-number">{props.counter}</div>
            <div className="description">of <span>{props.totalCount}</span></div>
        </div>
    </header>
);

export default QuestionCount;
