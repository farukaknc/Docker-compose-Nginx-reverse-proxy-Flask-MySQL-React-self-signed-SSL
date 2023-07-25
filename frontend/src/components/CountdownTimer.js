import React from 'react';


const DateTimeDisplay = ({ value, type, isDanger }) => {
    return (
        <div className={isDanger ? 'countdown danger' : 'countdown'}>
            <p>{value}</p>
            <span>{type}</span>
        </div>
    );
};



const ShowCounter = ({ hours, minutes, seconds }) => {
    return (
        <div className="show-counter">
            <div
                /*href="https://tapasadhikary.com"
                target="_blank"
                rel="noopener noreferrer"*/
                className="countdown-link"
            >
                <DateTimeDisplay value={hours} type={'Hours'} isDanger={false} />
                <p>:</p>
                <DateTimeDisplay value={minutes} type={'Mins'} isDanger={minutes < 1} />
                <p>:</p>
                <DateTimeDisplay value={seconds} type={'Seconds'} isDanger={minutes < 1} />
            </div>
        </div>
    );
};

const CountdownTimer = props => {

    return (
        <ShowCounter
            hours={props.hours}
            minutes={props.minutes}
            seconds={props.seconds}
        />
    );

};

export default CountdownTimer;