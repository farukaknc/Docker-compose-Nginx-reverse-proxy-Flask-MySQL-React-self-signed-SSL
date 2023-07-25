import React from "react";

const AnswerOptions = props => (
    <li className="answerOption">
        <input
            type="radio"
            className="radioCustomButton"
            name="radioGroup"
            onClick={props.onClick}
            checked={props.selectedOption === props.answerContent}
            value={props.answerContent}
            disabled={props.answer}
        /*onChange={props.onAnswerSelected}*/
        />
        <label className="radioCustomLabel" onClick={() => props.onClick(props.answerContent)}>
            {props.answerContent}
        </label>
    </li>
);

export default AnswerOptions;