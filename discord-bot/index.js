require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent]
});

client.once('ready', () => {
  console.log(`Bot online como ${client.user.tag}`);
});

client.on('messageCreate', async (message) => {
  if (message.author.bot) return;

  const content = message.content.toLowerCase();

  if (content === '!liberar guerra') {
    const channel = message.guild.channels.cache.find(c => c.name === 'guerra');
    if (!channel) return message.reply('Canal #guerra não encontrado.');

    await channel.permissionOverwrites.edit(message.guild.roles.everyone, {
      SendMessages: true
    });

    message.reply('Canal #guerra foi **liberado** para todos os membros.');
  }

  if (content === '!fechar guerra') {
    const channel = message.guild.channels.cache.find(c => c.name === 'guerra');
    if (!channel) return message.reply('Canal #guerra não encontrado.');

    await channel.permissionOverwrites.edit(message.guild.roles.everyone, {
      SendMessages: false
    });

    message.reply('Canal #guerra foi **fechado** para os membros.');
  }
});

client.login(process.env.DISCORD_TOKEN);
