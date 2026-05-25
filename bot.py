<?php
$token = "8009274939:AAHy-17cd-WkEMKEtYPlRgeys2oO_6Fg2Cc";
$admin_id = "8355555243";

$input = file_get_contents('php://input');
$update = json_decode($input);
if (!$update) exit;

$main_menu_inline = json_encode(['inline_keyboard' => [
    [['text' => '🟢 خرید اشتراک 🟢', 'callback_data' => 'pre_buy_types']],
    [['text' => '👤 حساب کاربری', 'callback_data' => 'main_acc'], ['text' => '📞 پشتیبانی', 'callback_data' => 'main_sup']]
]]);

if (isset($update->message)) {
    $msg = $update->message; $chat_id = $msg->chat->id; $text = $msg->text;

    if ($text == "/start") {
        send_message($chat_id, "به فروشگاه فیلترشکن سی‌تو خوش آمدید.\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:", $main_menu_inline);
    } 
    elseif (isset($msg->photo)) {
        $ph_id = end($msg->photo)->file_id;
        send_message($chat_id, "⏳ فیش دریافت شد. منتظر تایید مدیریت باشید.");
        
        $adm_btns = json_encode(['inline_keyboard' => [[
            ['text' => "✅ تایید فیش", 'callback_data' => "conf_{$chat_id}"], 
            ['text' => "❌ رد فیش", 'callback_data' => "rej_$chat_id"]
        ]]]);
        send_photo($admin_id, $ph_id, "🔔 فیش جدید!\n🆔 آیدی: $chat_id", $adm_btns);
    }
    
    if (isset($text) && $chat_id == $admin_id && isset($msg->reply_to_message)) {
        $reply_text = $msg->reply_to_message->text;
        if (strpos($reply_text, "شناسه:") !== false) {
            $u_id = trim(explode("شناسه:", $reply_text)[1]);
            $msg_to_user = "✅ واریزی شما تایید شد!\n\n🚀 لینک اختصاصی شما:\n\n`$text` \n\n👆 روی لینک بزنید تا کپی شود.";
            $after_link_btns = json_encode(['inline_keyboard' => [
                [['text' => "🛠 برنامه لازم برای کانفیگ", 'callback_data' => "help_usage"], ['text' => "🛒 خرید اشتراک جدید", 'callback_data' => 'pre_buy_types']]
            ]]);
            send_message($u_id, $msg_to_user, $after_link_btns);
            send_message($admin_id, "✅ لینک با موفقیت برای کاربر $u_id ارسال شد.");
        }
    }
}

if (isset($update->callback_query)) {
    $cb = $update->callback_query; $data = $cb->data; $cid = $cb->message->chat->id; $mid = $cb->message->message_id;

    // انتخاب نوع اشتراک (حجمی یا نامحدود)
    if ($data == "pre_buy_types") {
        $inline = json_encode(['inline_keyboard' => [
            [['text' => "📊 اشتراک حجمی", 'callback_data' => "type_hajmi"], ['text' => "♾ اشتراک نامحدود", 'callback_data' => "type_unlimit"]],
            [['text' => "🔙 بازگشت به منوی اصلی", 'callback_data' => "back_to_start"]]
        ]]);
        edit_message($cid, $mid, "🥇 لطفاً نوع اشتراک مورد نظر خود را انتخاب کنید:", $inline);
    }
    // بعد از انتخاب حجمی -> دکمه یک‌ماهه بیاید
    elseif ($data == "type_hajmi") {
        $inline = json_encode(['inline_keyboard' => [
            [['text' => "📅 یک‌ماهه", 'callback_data' => "show_hajmi_prices"]],
            [['text' => "🔙 بازگشت", 'callback_data' => "pre_buy_types"]]
        ]]);
        edit_message($cid, $mid, "⏱ مدت زمان اشتراک حجمی را انتخاب کنید:", $inline);
    }
    // بعد از انتخاب نامحدود -> دکمه یک‌ماهه بیاید
    elseif ($data == "type_unlimit") {
        $inline = json_encode(['inline_keyboard' => [
            [['text' => "📅 یک‌ماهه", 'callback_data' => "show_unlimit_prices"]],
            [['text' => "🔙 بازگشت", 'callback_data' => "pre_buy_types"]]
        ]]);
        edit_message($cid, $mid, "⏱ مدت زمان اشتراک نامحدود را انتخاب کنید:", $inline);
    }
    // نمایش لیست قیمت‌های حجمی یک‌ماهه
    elseif ($data == "show_hajmi_prices") {
        $inline = json_encode(['inline_keyboard' => [
            [['text' => "۳۰ مگ ◂ تست ۲۰ هزار تومان", 'callback_data' => "buy_30MB-Test_۲۰-هزار-تومان"]],
            [['text' => "۱ گیگ ◂ ۲۰۰ هزار تومان دو کاربر", 'callback_data' => "buy_1GB-2User_۲۰۰-هزار-تومان"]],
            [['text' => "۵ گیگ ◂ ۱ میلیون تومان دو کاربر", 'callback_data' => "buy_5GB-2User_۱-میلیون-تومان"]],
            [['text' => "۱۰ گیگ ◂ ۲ میلیون تومان دو کاربر", 'callback_data' => "buy_10GB-2User_۲-میلیون-تومان"]],
            [['text' => "۱۵ گیگ ◂ ۳ میلیون تومان دو کاربر", 'callback_data' => "buy_15GB-2User_۳-میلیون-تومان"]],
            [['text' => "۲۰ گیگ ◂ ۴ میلیون تومان دو کاربر", 'callback_data' => "buy_20GB-2User_۴-میلیون-تومان"]],
            [['text' => "🔙 بازگشت", 'callback_data' => "type_hajmi"]]
        ]]);
        edit_message($cid, $mid, "🥇 لیست قیمت‌های اشتراک حجمی (یک‌ماهه):", $inline);
    }
    // نمایش لیست قیمت‌های نامحدود یک‌ماهه
    elseif ($data == "show_unlimit_prices") {
        $inline = json_encode(['inline_keyboard' => [
            [['text' => "نامحدود یک کاربر ◂ ۴ میلیون تومان", 'callback_data' => "buy_Unlimited-1User_۴-میلیون-تومان"]],
            [['text' => "نامحدود دو کاربر ◂ ۲ میلیون تومان", 'callback_data' => "buy_Unlimited-2User_۲-میلیون-تومان"]],
            [['text' => "🔙 بازگشت", 'callback_data' => "type_unlimit"]]
        ]]);
        edit_message($cid, $mid, "🥇 لیست قیمت‌های اشتراک نامحدود (یک‌ماهه):", $inline);
    }
    elseif ($data == "main_acc") {
        $username = isset($cb->from->username) ? "@" . $cb->from->username : "ثبت نشده";
        $acc_text = "👤 حساب کاربری شما:\n\n💎 نام کاربری: $username\n🆔 آیدی عددی: `$cid` \n📍 وضعیت: آماده خرید";
        edit_message($cid, $mid, $acc_text, json_encode(['inline_keyboard' => [[['text' => "🔙 بازگشت", 'callback_data' => "back_to_start"]]]]));
    }
    elseif ($data == "main_sup") {
        edit_message($cid, $mid, "💎 پشتیبانی سی‌تو: @vpnsito\n\nسوالات و مشکلات خود را با ما در میان بگذارید.", json_encode(['inline_keyboard' => [[['text' => "🔙 بازگشت", 'callback_data' => "back_to_start"]]]]));
    }
    elseif ($data == "back_to_start") {
        edit_message($cid, $mid, "به فروشگاه فیلترشکن سی‌تو خوش آمدید.\nیکی از گزینه‌های زیر را انتخاب کنید:", $main_menu_inline);
    }
    elseif ($data == "help_usage") {
        $app_list = "✅ اشتراک‌های ما تمام برنامه‌های زیر رو پشتیبانی می‌کنه:\n\n" .
                    "🟢 V2RAY\n" .
                    "🟢 V2BOX\n" .
                    "🟢 V2RAY NG\n" .
                    "🟢 V2RAY tun\n" .
                    "🟢 Hiddify\n" .
                    "🟢 Happ";
        send_message($cid, $app_list, $main_menu_inline);
    }
    elseif (strpos($data, "buy_") !== false) {
        $ex = explode("_", $data); 
        $name = str_replace("-", " ", $ex[1]); 
        $price = str_replace("-", " ", $ex[2]);
        $pay_text = "✅ **طرح انتخاب شده:** $name\n💰 **مبلغ قابل پرداخت:** $price\n\n" .
                    "➖➖➖➖➖➖➖➖➖➖\n💳 شماره کارت جهت واریز:\n`6219861814211347`\n👤 **بنام:** مهین سراقی\n" .
                    "➖➖➖➖➖➖➖➖➖➖\n\n💡 *برای کپی آسان، روی شماره کارت بالا بزنید.*\n\n👇 **لطفاً پس از واریز، تصویر فیش را اینجا ارسال کنید:**";
        
        // تشخیص بازگشت دکمه پرداخت به منوی قیمتی مربوطه
        $back_callback = (strpos($data, "Unlimited") !== false) ? "show_unlimit_prices" : "show_hajmi_prices";
        
        edit_message($cid, $mid, $pay_text, json_encode(['inline_keyboard' => [[['text' => "🔙 بازگشت", 'callback_data' => $back_callback]]]]));
    }
    elseif (strpos($data, "conf_") !== false) {
        $u_id = str_replace("conf_", "", $data);
        send_message($admin_id, "لینک را روی این پیام ریپلای کنید:\nشناسه: $u_id");
    }
    elseif (strpos($data, "rej_") !== false) {
        send_message(str_replace("rej_", "", $data), "❌ فیش تایید نشد.");
    }
    
    call_api("answerCallbackQuery", ['callback_query_id' => $cb->id]);
}

function send_message($c, $t, $m = null) { return call_api("sendMessage", ['chat_id' => $c, 'text' => $t, 'parse_mode' => 'Markdown', 'reply_markup' => $m]); }
function send_photo($c, $p, $cap, $m = null) { return call_api("sendPhoto", ['chat_id' => $c, 'photo' => $p, 'caption' => $cap, 'reply_markup' => $m]); }
function edit_message($c, $mid, $t, $m = null) { return call_api("editMessageText", ['chat_id' => $c, 'message_id' => $mid, 'text' => $t, 'parse_mode' => 'Markdown', 'reply_markup' => $m]); }
function call_api($method, $post) {
    global $token; $u = "https://api.telegram.org/bot$token/$method";
    $ch = curl_init(); curl_setopt($ch, CURLOPT_URL, $u); curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post); curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $r = curl_exec($ch); curl_close($ch); return $r;
}
?>        $name = str_replace("-", " ", $ex[1]); 
        $price = str_replace("-", " ", $ex[2]);
        $pay_text = "✅ **طرح انتخاب شده:** $name\n💰 **مبلغ قابل پرداخت:** $price\n\n" .
                    "➖➖➖➖➖➖➖➖➖➖\n💳 شماره کارت جهت واریز:\n`6219861814211347`\n👤 **بنام:** مهین سراقی\n" .
                    "➖➖➖➖➖➖➖➖➖➖\n\n💡 *برای کپی آسان، روی شماره کارت بالا بزنید.*\n\n👇 **لطفاً پس از واریز، تصویر فیش را اینجا ارسال کنید:**";
        
        // تشخیص بازگشت دکمه پرداخت به منوی قیمتی مربوطه
        $back_callback = (strpos($data, "Unlimited") !== false) ? "show_unlimit_prices" : "show_hajmi_prices";
        
        edit_message($cid, $mid, $pay_text, json_encode(['inline_keyboard' => [[['text' => "🔙 بازگشت", 'callback_data' => $back_callback]]]]));
    }
    elseif (strpos($data, "conf_") !== false) {
        $u_id = str_replace("conf_", "", $data);
        send_message($admin_id, "لینک را روی این پیام ریپلای کنید:\nشناسه: $u_id");
    }
    elseif (strpos($data, "rej_") !== false) {
        send_message(str_replace("rej_", "", $data), "❌ فیش تایید نشد.");
    }
    
    call_api("answerCallbackQuery", ['callback_query_id' => $cb->id]);
}

function send_message($c, $t, $m = null) { return call_api("sendMessage", ['chat_id' => $c, 'text' => $t, 'parse_mode' => 'Markdown', 'reply_markup' => $m]); }
function send_photo($c, $p, $cap, $m = null) { return call_api("sendPhoto", ['chat_id' => $c, 'photo' => $p, 'caption' => $cap, 'reply_markup' => $m]); }
function edit_message($c, $mid, $t, $m = null) { return call_api("editMessageText", ['chat_id' => $c, 'message_id' => $mid, 'text' => $t, 'parse_mode' => 'Markdown', 'reply_markup' => $m]); }
function call_api($method, $post) {
    global $token; $u = "https://api.telegram.org/bot$token/$method";
    $ch = curl_init(); curl_setopt($ch, CURLOPT_URL, $u); curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post); curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $r = curl_exec($ch); curl_close($ch); return $r;
}
?>
