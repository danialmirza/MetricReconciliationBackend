function Helloreact() {
    return <div>Hello React!</div>;
}

ReactDom.render(<Helloreact />,
    document.getElementById('mountIt')
);