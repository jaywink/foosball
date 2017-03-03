import React from 'react';

class Players extends React.Component {
    render() {
        var players = ["Jaakko", "Kalle"];
        return (
            <div>
                List of players.
                <ul>
                    {players.map(function (name, index) {
                        return <li key={ index }>{name}</li>;
                    })}
                </ul>
            </div>
        );
    }
}

export default Players;
