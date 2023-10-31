const Sequelize = require("sequelize");
const bcrypt = require("bcryptjs");

const sequelize = new Sequelize({
    dialect: "sqlite",
    storage: "./storage.db",
    define: {
        timestamps: false,
    },
});

const news = [
    {
        title: "One Srdnlen in TeamItaly",
        news: "Riccardo Sulis is the first Sardinian CTF Player to join Team Italy in Lucca.",
        img: "DonRick.jpg",
        data: "15/09/2023",
        type: "italian",
        reserved: false,
    },
    {
        title: "Team Europe wins Internation Cybersecurity Championship",
        news: "Team Europe is confirmed as World Champion in the International competition held in San Diego.",
        img: "TeamEurope.jpg",
        data: "01/12/2022",
        type: "world",
        reserved: false,
    },
    {
        title: "2nd place at TeamItaly CTF 2023 for Srdnlen",
        news: "Second place at the great Team Italy CTF 2023 after 24H of competition. A very good results for Srdnlen which was surpassed by National Denmark Team (European CyberSecurity Challenge 2022 champion) one step away from victory!",
        img: "TeamSrdnlen.jpeg",
        data: "01/10/2023",
        type: "italian",
        reserved: false,
    },
    {
        title: "CyberCup.IT 2023",
        news: "A great first edition of CyberCup.IT is just concluded. The podium consists of the best Italian CTF Teams. \
        \t 1°. Tower of Hanoi;\t 2°. Srdnlen;\t 3°. MadrHacks;",
        img: "srdnlen.jpg",
        data: "01/07/2023",
        type: "italian",
        reserved: false,
    },
    {
        title: "FLAG",
        news: process.env["FLAG"] || "srdnlen{flag}",
        img: "flag.png",
        data: "28/10/2023",
        type: "world",
        reserved: true,
    },
];

const Database = {};

Database.sequelize = sequelize;

Database.Users = sequelize.define("users", {
    id: {
        type: Sequelize.INTEGER,
        autoIncrement: true,
        primaryKey: true,
        allowNull: false,
        unique: true,
    },
    username: {
        type: Sequelize.STRING,
        allowNull: false,
        unique: true,
    },
    password: {
        type: Sequelize.STRING,
        allowNull: false,
    },
});

Database.News = sequelize.define("news", {
    id: {
        type: Sequelize.INTEGER,
        autoIncrement: true,
        primaryKey: true,
        allowNull: false,
    },
    title: {
        type: Sequelize.STRING,
        allowNull: false,
        unique: true,
    },
    news: {
        type: Sequelize.STRING,
        allowNull: false,
        unique: true,
    },
    img: {
        type: Sequelize.STRING,
        allowNull: false,
    },
    data: {
        type: Sequelize.STRING,
        allowNull: false,
        unique: false,
    },
    type: {
        type: Sequelize.STRING,
        allowNull: false,
    },
    reserved: {
        type: Sequelize.BOOLEAN,
        allowNull: false,
        unique: false,
    },
});

Database.connect = async () => {
    try {
        await sequelize.authenticate();
    } catch (error) {
        console.error("Unable to connect to the database:", error);
    }
};

Database.create = async () => {
    try {
        await Database.Users.sync({ force: true });
        await Database.News.sync({ force: true });
        await Database.Users.create({
            username: "admin",
            password: bcrypt.hashSync(
                process.env["ADMIN_PASSWORD"] || "password",
                10,
            ),
        });

        news.forEach(async (news) => {
            await Database.News.create(news);
        });
    } catch (error) {
        console.error("Error creating table:", error);
    }
};

module.exports = Database;
